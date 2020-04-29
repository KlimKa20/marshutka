from django.test import TestCase
from .models import Articles

class TestModel(TestCase):

    def test_Station(self):
        artickles = Articles.objects.create(title="GGG", date ='2020-12-12')
        assert artickles.__str__() == 'GGG'
