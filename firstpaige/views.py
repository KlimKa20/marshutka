from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings

from firstpaige.models import Comment


def index(request):
    if request.method == 'POST':
        if 'new_comment' in request.POST:
            comment = Comment()
            comment.comment = request.POST['Text']
            comment.user = request.user
            comment.save()
        else:
            message = 'Имя пользователя: ' + request.POST['Name'] + '\n' + request.POST[
                'message'] + '\n' + 'Email для связи: ' + request.POST['Email']
            send_mail('Novolukoml_Minsk',
                      message,
                      settings.EMAIL_HOST_USER,
                      ['novolukoml_minsk@mail.ru'],
                      fail_silently=False)

    instance = Comment.objects.all()
    data = {"comments": instance}
    return render(request, 'firstpage.html', context=data)
