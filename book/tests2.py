from django.test import TestCase, Client
from .models import Station, Car, Schedule, Seat_Chart, Ticket
from django.contrib.auth.models import User
from .apps import BookConfig
import pytest


@pytest.fixture
def test_user(db):
    user = User.objects.create_user('John', 'Lennon@thebeatles.com', 'johnpassword')
    user.save()
    return user


@pytest.fixture
def test_data(db):
    station = Station.objects.create(name='Minsk', code='0')
    station.save()
    station2 = Station.objects.create(name='Minsk2', code='1')
    station2.save()
    car = Car.objects.create(dest=station, source=station2)
    car.save()
    seat = Seat_Chart.objects.create(car=car, first_ac=1, second_ac=2, date='2020-12-12')
    seat.save()
    schedule = Schedule.objects.create(id=1, car=car, station=station)
    schedule.save()
    schedule2 = Schedule.objects.create(id=2, car=car, station=station2)
    schedule2.save()
    return station, station2, car, seat, schedule, schedule2


def test_home(db, test_user):
    c = Client()
    c.login(username='John', password='johnpassword')
    response = c.post('/marshrutka/')
    assert response.status_code == 200


def test_searchView(db, test_user, test_data):
    c = Client()
    c.login(username='John', password='johnpassword')
    station, station2, car, seat, schedule, schedule2 = test_data
    response = c.post('/marshrutka/search', {'source': station.pk, 'dest': station2.pk, 'journey_date': '2020-12-12'})
    assert response.status_code == 200
    response = c.post('/marshrutka/complexSearch/0-1/2020-12-12',
                      {'source': station.pk, 'dest': station2.pk, 'journey_date': '2020-12-12'})
    assert response.status_code == 200
    user = test_user
    response = c.post('/marshrutka/book/1/1-2/1A/2020-12-12', {'chart': seat.pk, 'sourceSchedule': station.pk, 'destSchedule': station2.pk, 'type': '1A', 'date': '2020-12-12'})
    assert response.status_code == 200
    response = c.post('/marshrutka/book/1/1-2/2A/2020-12-12',
                      {'chart': seat.pk, 'sourceSchedule': station.pk, 'destSchedule': station2.pk, 'type': '2A',
                       'date': '2020-12-12'})
    assert response.status_code == 200
    response = c.post('/marshrutka/confirm/1/1-2/2A/2020-12-12',
                      {'chart': seat.pk, 'sourceSchedule': station.pk, 'destSchedule': station2.pk, 'type': '2A',
                       'date': '2020-12-12', 'seats': 1, 'name0':'Alina'})
    assert response.status_code == 200
    ticket = Ticket.objects.create(passenger='Alina', car=car, type='1A', chart=seat, source=station, dest=station2,
                                   source_schedule=schedule, dest_schedule=schedule2, date='2020-12-12', fare=20,
                                   user=user)
    ticket.save()
    response = c.post('/marshrutka/profile')
    assert response.status_code == 200


@pytest.mark.parametrize("app", [BookConfig.name])
@pytest.mark.parametrize("expected", ['book'])
def test_app(app, expected):
    assert app == expected
