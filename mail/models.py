from django.core.mail import EmailMessage
from django.db import models
from accounts.models import Profile
from django.template.loader import render_to_string
from multiprocessing.pool import ThreadPool


class Mail(models.Model):
    id = models.AutoField(primary_key=True)
    topic = models.CharField(max_length=120)
    text = models.TextField()
    datetime = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(Profile, limit_choices_to={'Verified': True}, blank=False)
    check_send = models.BooleanField(default=False)

    def __str__(self):
        if self.check_send is False:
            self.check_send = True
            self.send()
            self.save()
        return str(self.topic)

    def send(self):
        message = render_to_string('accounts/mail.html', {
            'text': self.text,
            'date': self.date,
            'time': self.time
        })
        mail_subject = self.topic
        mount = self.users.count()
        pool_executor = ThreadPool(mount)
        result = []
        for profile in self.users.all():
            to_email = profile.user.email
            email = EmailMessage(
                mail_subject, message, to=[to_email])
            result.append(email)

        pool_executor.map(send_mail, result)


def send_mail(email):
    email.send()
