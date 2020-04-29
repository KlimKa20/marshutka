from django.test import TestCase
from .models import Mail


class TestModel(TestCase):

    def test_Mail(self):
        mail = Mail.objects.create(topic="GGG", text='aaaaa', date='2020-12-12', time='11:11:11', check_send=True)
        assert mail.__str__() == 'GGG'
