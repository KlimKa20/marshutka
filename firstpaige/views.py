from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings


def index(request):
    if request.method == 'POST':
        message = 'Имя пользователя: ' + request.POST['Name'] + '\n' + request.POST['message'] + '\n' + 'Email для связи: ' + request.POST['Email']
        send_mail('Novolukoml_Minsk',
                  message,
                  settings.EMAIL_HOST_USER,
                  ['novolukoml_minsk@mail.ru'],
                  fail_silently=False)
    return render(request, 'firstpage.html')