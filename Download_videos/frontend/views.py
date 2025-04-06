from django.shortcuts import render



def angular_app(request):
    return render(request, 'registration_form.html')
