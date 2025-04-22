import requests
from django.http import HttpResponseRedirect
from regform.models import People
from django.shortcuts import render, redirect


def index_1(request):
    if request.method == 'POST':
        login = request.POST['username']
        password = request.POST['password']
        body = {
            'username': login,
            'password': password
        }
        url = 'http://127.0.0.1:1278/register/'
        response = requests.post(url, data=body)
        if response.status_code == 201:
            return redirect("login/")
        else:
            print('Error: User already exists or other issue')
            return render(request, 'registration_form.html',
                          {'error': 'User already exists or there was a problem with registration.'})

    return render(request, 'registration_form.html')


def congrat(request):
    return render(request, 'congratulations.html')


def login_page(request):
    if request.method == 'POST':

        given_login = request.POST.get('username')
        given_pass = request.POST.get('password')

        body = {
            'username': given_login,
            'password': given_pass
        }
        url = 'http://127.0.0.1:1278/api/login/'
        response = requests.post(url, data=body)
        token = response.json()['token']

        with open('token.txt', 'wt') as file:
            file.write(token)

        if response.status_code == 200:
            return HttpResponseRedirect('/congrat')
        else:
            return render(request, 'login.html', {'error': 'Registration failed or user already exists.'})

    return render(request, 'login.html')
