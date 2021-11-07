from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.

class Station(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField("Code", max_length=15)
    name = models.CharField("Name", max_length=30)
    address = models.CharField("Address", max_length=50, null=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Car(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField("Name", max_length=30)
    number = models.CharField("Number", max_length=15)
    source = models.ForeignKey(Station, on_delete=models.SET(None), related_name="car_source")
    dest = models.ForeignKey(Station, on_delete=models.SET(None), related_name="car_dest")

    def __str__(self):
        return self.name


class Schedule(models.Model):
    id = models.AutoField(primary_key=True)
    day = models.DateField("Day", null=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="car_schedule")
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="station_schedule")
    departure = models.TimeField("Departure", null=True)
    arrival = models.TimeField("Arrival", null=True)

    def __str__(self):
        return str(self.car) + " at " + str(self.station)

    def getStationName(self):
        return self.station.name


class SeatChart(models.Model):
    id = models.AutoField(primary_key=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="car_chart")
    first_ac = models.IntegerField("1st AC")
    second_ac = models.IntegerField("2nd AC")
    date = models.DateField("Date")

    def get1A(self):
        type = TypeSeat.objects.get(type='1A')
        return self.first_ac - self.chart_tickets.all().filter(type=type).count()

    def get2A(self):
        type = TypeSeat.objects.get(type='2A')
        return self.second_ac - self.chart_tickets.all().filter(type=type).count()

    def __str__(self):
        return str(self.car) + " on " + str(self.date)


class TypeSeat(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField("Type", max_length=2)

    def __str__(self):
        return str(self.type)


class Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    passenger = models.CharField("Name", max_length=20)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="car_tickets")
    type = models.ForeignKey(TypeSeat, on_delete=models.CASCADE, related_name="type_chart")
    chart = models.ForeignKey(SeatChart, on_delete=models.CASCADE, related_name="chart_tickets")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets")
    source = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name="source_schedule_tickets")
    dest = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name="dest_schedule_tickets")
    datetime = models.DateTimeField(auto_now=True)
    fare = models.IntegerField("Fare")

    def __str__(self):
        return str(self.passenger) + " on " + str(self.date)+" in "+str(self.car)

    def calculateFare(self):
        factor = 1
        type = self.type.type
        if type == "1A":
            factor = 20
        elif type == "2A":
            factor = 15
        self.fare = (self.dest.pk - self.source.pk)*factor
