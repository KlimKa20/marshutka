from django.test import TestCase, Client
from .apps import FirstpaigeConfig
from django.apps import AppConfig

class TestView(TestCase):
    def test_index(self):
        c = Client()
        response = c.post('/', {'Name': 'aa', 'message': 'aaaa', 'Email': "aaa"})
        assert response.status_code == 200

    def test_app(self):
        app = FirstpaigeConfig
        assert app.name == 'firstpaige'