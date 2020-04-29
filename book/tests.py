from django.test import TestCase, Client
from .models import Station, Car, Schedule, Seat_Chart,Ticket
from django.contrib.auth.models import User
import json


class TestModel(TestCase):

    def test_Station(self):
        station = Station.objects.create()
        station.name = 'Minsk'
        station.save()
        assert station.__str__() == 'Minsk'

    def test_Car(self):
        station = Station.objects.create()
        station.name = 'Minsk'
        station.save()
        car = Car.objects.create(dest=station, source=station)
        car.name = 'Minsk'
        car.save()
        assert car.__str__() == 'Minsk'

    def test_Schedule(self):
        station = Station.objects.create()
        station.name = 'Minsk'
        station.save()
        car = Car.objects.create(dest=station, source=station)
        schedule = Schedule.objects.create(id='1', car=car, station=station)
        assert schedule.__str__()==' at Minsk'

    def test_Seat_Chart(self):
        station = Station.objects.create()
        station.name = 'Minsk'
        station.save()
        car = Car.objects.create(dest=station, source=station)
        seat = Seat_Chart.objects.create(car=car, first_ac=1, second_ac=2, date='2020-12-12')
        seat.get2A()
        seat.get1A()
        assert seat.__str__() == ' on 2020-12-12'

    def test_Ticket(self):
        station = Station.objects.create(name='Minsk')
        station2 = Station.objects.create(name='Minsk2', code='1')
        user = User.objects.create_user('John', 'Lennon@thebeatles.com', 'johnpassword')
        car = Car.objects.create(dest=station, source=station)
        seat = Seat_Chart.objects.create(car=car, first_ac=1, second_ac=2, date='2020-12-12')
        schedule = Schedule.objects.create(id=1, car=car, station=station)
        schedule2 = Schedule.objects.create(id=2, car=car, station=station2)
        ticket = Ticket.objects.create(passenger='Alina', car=car, type='1A', chart=seat, source=station, dest=station2, source_schedule=schedule, dest_schedule=schedule2, date='2020-12-12', fare=20, user=user)
        ticket.calculateFare()
        ticket2 = Ticket.objects.create(passenger='Alina', car=car, type='2A', chart=seat, source=station, dest=station2, source_schedule=schedule, dest_schedule=schedule2, date='2020-12-12', fare=20, user=user)
        ticket2.calculateFare()
        assert ticket.__str__() == 'Alina on 2020-12-12 in '

