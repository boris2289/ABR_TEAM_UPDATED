import os
import shutil

from pytubefix import YouTube, exceptions
import pytubefix as pb
from link_collector.models import Resolution
from django.views.decorators.csrf import csrf_exempt
from link_collector.models import Mistakes, Link
from django.shortcuts import render
from tqdm import tqdm
from moviepy.editor import VideoFileClip, AudioFileClip
import requests

mistakes = Mistakes()
resolution = Resolution()
mistakes.mistakes['empty_link'], mistakes.mistakes['age_restriction'] = False, False
Link = Link()


def link_inserting(link):
    video_link = YouTube(link, use_oauth=False, allow_oauth_cache=False)
    streams = video_link.streams
    resolutions = set()
    for stream in streams:
        resolutions.add(stream.resolution)
    current_resol = Resolution()
    current_resol.resolution = sorted([i for i in list(resolutions) if i is not None],
                                      key=lambda x: int(x.split('p')[0]))
    return current_resol.resolution

@csrf_exempt
def form1_view(request):
    mistakes.mistakes['empty_link'], mistakes.mistakes['age_restriction'] = False, False
    if request.method == 'POST':
        Link.link = request.POST.get('link', '')
        try:
            response = requests.get(Link.link)
            if response.status_code != 200:
                mistakes.mistakes['empty_link'] = True
        except requests.exceptions.RequestException:
            mistakes.mistakes['empty_link'] = True
        if not Link.link:
            mistakes.mistakes['empty_link'] = True
        else:
            if mistakes.mistakes['empty_link'] is False:
                try:
                    resolution.resolution = link_inserting(Link.link)
                except (pb.exceptions.AgeRestrictedError, pb.exceptions.RegexMatchError):
                    mistakes.mistakes['age_restriction'] = True
    return render(request, 'loadfile.html', {'resol': resolution.resolution, 'mistakes': mistakes.mistakes})


def form2_view(request):
    mp4, progres = False, False
    if request.method == 'POST':
        action = request.POST.get('data_name', '').rstrip()
        path = './'
        if 'videos' not in os.listdir(path):
            makedir(path)
        if 'audios' not in os.listdir(path):
            os.mkdir(path=f'{path}/audios')
        new_path = './videos'
        audio_path = './audios'
        if YouTube(Link.link).streams.filter(res=action, progressive=True, file_extension='mp4').first() is not None:
            mp4 = True
            progres = True
        elif YouTube(Link.link).streams.filter(res=action, progressive=True).first() is not None:
            progres = True
        download(Link.link, action, mp4, progres, new_path, audio_path)
        change_extension(new_path, audio_path)
        mistakes.mistakes['empty_link'], mistakes.mistakes['age_restriction'] = False, False
    return render(request, 'loadfile.html', {'resol': resolution.resolution, 'mistakes': mistakes.mistakes})


def download_audio(link, audio_path):
    YouTube(link).streams.filter(only_audio=True).first().download(output_path=audio_path)


def download(link, action, mp4, progres, new_path, audio_path):
    file_size = YouTube(Link.link).streams.filter(res=action).first().filesize
    progress_bar = tqdm(total=file_size, unit='B', unit_scale=True)

    def progress_callback(stream, chunk, bytes_remaining):
        progress_bar.update(len(chunk))

    if mp4 is False:
        YouTube(Link.link, on_progress_callback=progress_callback).streams.filter(res=action,
                                                                                  progressive=progres).first().download(
            output_path=new_path)
    else:
        YouTube(Link.link, on_progress_callback=progress_callback).streams.filter(res=action, progressive=progres,
                                                                                  file_extension='mp4').first().download(
            output_path=new_path)
    if progres is False:
        download_audio(link, audio_path)
    progress_bar.close()


def change_extension(new_path, audio_path):
    for i in os.listdir(new_path):
        if i.split('.')[-1] == 'webm':
            output_file = f'{new_path}/{i.split(".")[:-1:][0]}.mp4'
            video = VideoFileClip(f'{new_path}/{i}')
            video.write_videofile(output_file, codec='libx264')
            os.remove(path=f'{new_path}/{i}')
    combine_video_audio(new_path, audio_path)


def combine_video_audio(new_path, audio_path):
    if 'My_Downloaded_videos' not in os.listdir('./'):
        os.mkdir(path='./My_Downloaded_videos')
    for i in os.listdir(f'{new_path}'):
        for j in os.listdir(f'{audio_path}'):
            if i.split('.')[0] == j.split('.')[0]:
                aud_path = f'{audio_path}/{i.replace(".mp4", ".m4a")}'
                vid_path = f'{new_path}/{i}'
                video = VideoFileClip(vid_path)
                audio = AudioFileClip(aud_path)
                audio = audio.set_duration(video.duration)
                video = video.set_audio(audio)
                pat = './My_Downloaded_videos'
                video.write_videofile(f'{pat}/{i}', codec="libx264", audio_codec='aac')

    if os.path.exists(audio_path) and os.path.isdir(audio_path):
        shutil.rmtree(audio_path)

    if os.path.exists(new_path) and os.path.isdir(new_path):
        shutil.rmtree(new_path)


def makedir(path):
    os.mkdir(path=f'{path}/videos')


def collector(request):
    mistakes.mistakes['empty_link'], mistakes.mistakes['age_restriction'] = False, False
    return render(request, 'loadfile.html', {'resol': resolution.resolution, 'mistakes': mistakes.mistakes})
