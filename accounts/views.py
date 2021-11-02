from __future__ import unicode_literals
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.contrib.auth import views as authviews
from braces import views as bracesviews
from django.conf import settings
from . import forms
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User


class LoginView(bracesviews.AnonymousRequiredMixin, authviews.LoginView):
    template_name = "accounts/login.html"
    form_class = forms.LoginForm


    def form_valid(self, form):
        r = super(LoginView, self).form_valid(form)
        remember_me = form.cleaned_data.get('remember_me')
        if remember_me is True:
            ONE_MONTH = 30*24*60*60
            expiry = getattr(settings, "KEEP_LOGGED_DURATION", ONE_MONTH)
            self.request.session.set_expiry(expiry)

        return redirect('book:home')


class LogoutView(authviews.LogoutView):
    url = reverse_lazy('book:home')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'accounts/activate.html')
    else:
        return HttpResponse('Activation link is invalid!')


def SignUpView(request):
    if request.method == 'GET':
        return render(request, 'accounts/signup.html')
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST or None)
       # print(form.errors.as_data())
        if form.is_valid():
            userValue = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password1Value = form.cleaned_data.get("password1")
            password2Value = form.cleaned_data.get("password2")
            context = {'form': form}
            if User.objects.filter(email=email).exists():
                context["error_mail"] = "Данная почта уже зарегестрирована"
            if password1Value != password2Value:
                context["error_password"] = "Пароли не совпадают"
            if len(context) == 1:
                user = User.objects.create_user(username=userValue, email=email, password = password2Value)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your account.'
                token = account_activation_token.make_token(user)
                message = render_to_string('accounts/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.id)).decode(),
                    'token': token,
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                return render(request, 'accounts/validation.html')
            else:
                return render(request, 'accounts/signup.html', context)
        else:
            context = {'form': form}
            if 'username' in form.errors.as_data():
                context["error_name"] = "Данное имя уже зарегестрировано"
            return render(request, 'accounts/signup.html', context)




class PasswordChangeView(authviews.PasswordChangeView):
    form_class = forms.PasswordChangeForm
    template_name = 'accounts/password-change.html'
    success_url = reverse_lazy('book:home')

    def form_valid(self, form):
        form.save()
        messages.success(self.request,
                         "Your password was changed, "
                         "You have been logged out. Please relogin")
        return super(PasswordChangeView, self).form_valid(form)
