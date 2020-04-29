from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from accounts.forms import LoginForm, SignUpForm, PasswordChangeForm
from .apps import AccountsConfig


class TestForm(TestCase):

    def test_app(self):
        app = AccountsConfig
        assert app.name == 'accounts'

    def test_valid_login_form(self):
            user = User.objects.create_user('John', 'Lennon@thebeatles.com', 'johnpassword')
            user.save()
            data = {'username': 'John', 'password': 'johnpassword'}
            form = LoginForm(data=data)
            self.assertTrue(form.is_valid())

    def test_invalid_login_form(self):
        data = {'username': "test_user2", 'password': "fdsgsdfgfdg"}
        form = LoginForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_signup_form(self):
        user = User.objects.create_user('John', 'Lennon@thebeatles.com', 'johnpassword')
        user.save()
        data = {'username': 'John', 'password1': 'johnpassword', 'password1': 'johnpassword',
                'email': "vjhgg@yandex.ru"}
        form = SignUpForm(data=data)
        self.assertFalse(form.is_valid())

    def test_signup_form(self):
        data = {'username': "test_user2", 'password1': "fdsgsdfgfdg", 'password2': "fdsgsdfgfdg",
                'email': 'alinasadovsckaya@yandex.ru', }
        form = SignUpForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_password_form(self):
        user = User.objects.create_user('John', 'Lennon@thebeatles.com', 'johnpassword')
        user.save()
        data = {'old_password': "notjohnpassword", 'new_password1': "fdsgsdfgfdg", 'new_password2': "fdsgsdfgfdg"}
        form = PasswordChangeForm(user=user, data=data)
        self.assertFalse(form.is_valid())

    def test_password_change_form(self):
        user = User.objects.create_user('John', 'Lennon@thebeatles.com', 'johnpassword')
        user.save()
        data = {'old_password': "johnpassword", 'new_password1': "fdsgsdfgfdg", 'new_password2': "fdsgsdfgfdg"}
        form = PasswordChangeForm(user=user, data=data)
        self.assertTrue(form.is_valid())


class TestModel(TestCase):
    def test_Profile(self):
        user = User.objects.create_user('John', 'Lennon@thebeatles.com', 'johnpassword')
        user.save()
        profile = user.profile
        assert profile.Verified == True

    def test_nonacive_Profile(self):
        user_nonactive = User.objects.create_user(' Paul', 'McCartney@thebeatles.com', 'paulpassword')
        user_nonactive.is_active=False
        user_nonactive.save()
        profile = user_nonactive.profile
        assert profile.Verified == False

    def test_Profile_rename(self):
        user = User.objects.create_user('Ringo', 'Star@thebeatles.com', 'ringopassword')
        user.save()
        user.is_active = False
        user.save()
        assert user.profile.Verified == False


class TestURL(TestCase):
    def test_login_url(self):
        path = reverse('accounts:login')
        assert resolve(path).view_name == 'accounts:login'

    def test_logout_url(self):
        path = reverse('accounts:logout')
        assert resolve(path).view_name == 'accounts:logout'

    def test_signup_url(self):
        path = reverse('accounts:signup')
        assert resolve(path).view_name == 'accounts:signup'

    def test_password_change_url(self):
        path = reverse('accounts:password-change')
        assert resolve(path).view_name == 'accounts:password-change'


class TestView(TestCase):
    def test_login_open_view(self):
        path = reverse('accounts:login')
        resp = self.client.get(path)
        self.assertEqual(resp.status_code, 200)

    def test_login_view_user(self):
        user = User.objects.create_user('John', 'Lennon@thebeatles.com', 'johnpassword')
        user.save()
        path = reverse('accounts:login')
        resp = self.client.get(path)
        form = resp.context['form']
        data = form.initial
        data['username'] = 'John'
        data['password'] = 'johnpassword'
        resp = self.client.post(path, data)
        self.assertEqual(resp.status_code, 302)

    def test_logout_view(self):
        path = reverse('accounts:logout')
        resp = self.client.get(path)
        self.assertEqual(resp.status_code, 302)

    def test_password_view(self):
        path = reverse('accounts:password-change')
        resp = self.client.get(path)
        self.assertEqual(resp.status_code, 302)

    def test_SignUpView_view(self):
        path = reverse('accounts:signup')
        resp = self.client.get(path)
        self.assertEqual(resp.status_code, 200)

    def test_registration(self):
        c = Client()
        response = c.post('/marshrutka/signup/')
        assert response.status_code == 200
        response = c.post('/marshrutka/signup/',
                          {'username': 'default', 'password1': 'default', 'password2': 'default',
                           'email': 'default@gmail.com'})
        assert response.status_code == 200
        response = c.post('/marshrutka/signup/',
                          {'username': 'default', 'password1': 'default', 'password2': 'default2',
                           'email': 'default@gmail.com'})
        assert response.status_code == 200

    def test_login(self):
        c = Client()
        user = User.objects.create_user('John', 'Lennon@thebeatles.com', 'johnpassword')
        user.save()
        response = c.post('/marshrutka/login/',
                          {'username': 'John', 'password': 'johnpassword', 'remember_me': 'True'})
        assert response.status_code == 302

