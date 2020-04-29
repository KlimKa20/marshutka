import logging
import traceback
from dateutil import parser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import *

logger = logging.getLogger('django')


@login_required(login_url="/marshrutka/login")
def homeView(request):
    stations = Station.objects.all()
    context = {
        "stations": stations,
        "st": stations[0:4]
    }
    return render(request, 'book/home.html', context)


@login_required(login_url="/marshrutka/login")
def searchView(request):
    source = Station.objects.get(pk=request.POST['source'])
    dest = Station.objects.get(pk=request.POST['dest'])
    date = request.POST['journey_date']
    sourceCars = []
    for s in source.station_schedule.all():
        sourceCars.append(s.car)
    destCars = []
    for s in dest.station_schedule.all():
        destCars.append(s.car)
    allCars = list(set(sourceCars) & set(destCars))
    cars = []
    sourceSchedules = []
    destSchedules = []
    scheduleCharts = []
    fares = []
    for t in allCars:
        departing_station = t.car_schedule.get(station=source)
        arriving_station = t.car_schedule.get(station=dest)
        if departing_station.pk < arriving_station.pk:
            try:
                seat = Seat_Chart.objects.get(date=parser.parse(date), car=t)
                scheduleCharts.append(seat)
                cars.append(t)
                sourceSchedules.append(departing_station)
                destSchedules.append(arriving_station)
                fare = {}
                fare["1A"] = (arriving_station.pk - departing_station.pk)*20
                fare["2A"] = (arriving_station.pk - departing_station.pk)*15
                fares.append(fare)
            except Exception:
                continue

    schedules = zip(cars, sourceSchedules, destSchedules, scheduleCharts, fares)
    temp=False
    if cars:
        temp = True
    data = {
        "source": source,
        "dest": dest,
        "schedules": schedules,
        "date": date,
        "flag": temp,
    }
    return render(request, 'book/trainSearch.html', data)


@login_required(login_url="/marshrutka/login")
def complexSearchView(request, source, dest, date):
    source = Station.objects.get(pk=source)
    dest = Station.objects.get(pk=dest)
    sourceCars = []
    for s in source.station_schedule.all():
        sourceCars.append(s.car)
    destCars = []
    for s in dest.station_schedule.all():
        destCars.append(s.car)
    allCars = list(set(sourceCars) & set(destCars))
    cars = []
    sourceSchedules = []
    destSchedules = []
    scheduleCharts = []
    fares = []
    for t in allCars:
        departing_station = t.car_schedule.get(station=source)
        arriving_station = t.car_schedule.get(station=dest)
        if departing_station.pk < arriving_station.pk:
            try:
                seat = Seat_Chart.objects.get(date=parser.parse(date), car=t)
                scheduleCharts.append(seat)
                cars.append(t)
                sourceSchedules.append(departing_station)
                destSchedules.append(arriving_station)
                fare = {}
                fare["1A"] = (arriving_station.pk - departing_station.pk) * 20
                fare["2A"] = (arriving_station.pk - departing_station.pk) * 15
                fares.append(fare)
            except Exception:
                continue

    schedules = zip(cars, sourceSchedules, destSchedules, scheduleCharts, fares)
    temp = False
    if cars:
        temp = True
    data = {"source": source, "dest": dest, "schedules": schedules, "date": date, "flag": temp}
    return render(request, 'book/connectingTrainSearch.html', data)


@login_required(login_url="/marshrutka/login")
def bookView(request, chart, sourceSchedule, destSchedule, type, date):
    chart = Seat_Chart.objects.get(pk=chart)
    car = chart.car
    sourceSchedule = Schedule.objects.get(pk=sourceSchedule)
    destSchedule = Schedule.objects.get(pk=destSchedule)
    source = sourceSchedule.station
    dest = destSchedule.station
    value = 0
    if type =="1A":
        value = chart.get1A()
    else:
        value = chart.get2A()
    data = {"car": car, "chart": chart, "sourceSchedule": sourceSchedule, "destSchedule": destSchedule, "source": source, "dest": dest, "type": type, "date": date, "value_seat": str(value)}
    return render(request, 'book/booking.html', data)


@login_required(login_url="/marshrutka/login")
def confirmTicketView(request, chart, sourceSchedule, destSchedule, type, date):
    chart = Seat_Chart.objects.get(pk=chart)
    car = chart.car
    sourceSchedule = Schedule.objects.get(pk=sourceSchedule)
    destSchedule = Schedule.objects.get(pk=destSchedule)
    source = sourceSchedule.station
    dest = destSchedule.station
    user = request.user
    seats = int(request.POST["seats"])
    for i in range(seats):
        name = request.POST.get("name"+str(i))
        b = Ticket()
        b.passenger = name
        b.car = car
        b.type = type
        b.chart = chart
        b.user = user
        b.source = source
        b.dest = dest
        b.source_schedule = sourceSchedule
        b.dest_schedule = destSchedule
        b.date = date
        b.calculateFare()
        b.save()
        logger.info("{name} Add ticket".format(name=name))


    data = {
        "car": car,
        "sourceSchedule": sourceSchedule,
        "destSchedule": destSchedule,
        "source": source,
        "dest": dest,
        "type": type
    }
    return render(request, 'book/home.html')


@login_required(login_url="/marshrutka/login")
def profileView(request):
    user = request.user
    booked = user.tickets.all()
    data = {
        "booked": booked,
    }
    return render(request, 'book/profile.html', data)


class cancelTicket(LoginRequiredMixin, DeleteView):
    login_url = '/marshrutka/login'
    model = Ticket
    success_url = reverse_lazy('book:profile')

    def dispatch(self, request, *args, **kwargs):
        pk = kwargs['pk']
        if request.user != Ticket.objects.get(pk=pk).user:
            return redirect('book:home')
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

