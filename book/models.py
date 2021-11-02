from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.

class Station(models.Model):
    code = models.CharField("Code", max_length=10, primary_key=True)
    name = models.CharField("Name", max_length=30)
    address = models.CharField("Address", max_length=50, null=True)

    def __str__(self):
        return self.name


class Car(models.Model):
    name = models.CharField("Name", max_length=30)
    number = models.CharField("Number", max_length=15, primary_key=True)
    source = models.ForeignKey(Station, on_delete=models.SET(None), related_name="car_source")
    dest = models.ForeignKey(Station, on_delete=models.SET(None), related_name="car_dest")

    def __str__(self):
        return self.name


class Schedule(models.Model):
    id = models.AutoField(primary_key=True)
    arrival = models.CharField("Arrival", max_length=8, null=True)
    day = models.IntegerField("Day", null=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="car_schedule")
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="station_schedule")
    departure = models.CharField("Departure", max_length=8, null=True)

    def __str__(self):
        return str(self.car) + " at " + str(self.station)


class Seat_Chart(models.Model):
    id = models.AutoField(primary_key=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="car_chart")
    first_ac = models.IntegerField("1st AC")
    second_ac = models.IntegerField("2nd AC")
    date = models.DateField("Date")

    def get1A(self):
        return self.first_ac - self.chart_tickets.all().filter(type="1A").count()

    def get2A(self):
        return self.second_ac - self.chart_tickets.all().filter(type="2A").count()

    def __str__(self):
        return str(self.car) + " on " + str(self.date)


class Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    passenger = models.CharField("Name",max_length=20)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="car_tickets")
    type = models.CharField("Type",max_length=2)
    chart = models.ForeignKey(Seat_Chart, on_delete=models.CASCADE, related_name="chart_tickets")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets")
    source = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="source_tickets")
    dest = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="dest_tickets")
    source_schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name="source_schedule_tickets")
    dest_schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name="dest_schedule_tickets")
    date = models.DateField("Date")
    fare = models.IntegerField("Fare")

    def __str__(self):
        return str(self.passenger) + " on " + str(self.date)+" in "+str(self.car)

    def calculateFare(self):
        factor=1
        if(self.type == "1A"):
            factor = 20
        elif(self.type == "2A"):
            factor = 15
        self.fare = (self.dest_schedule.pk - self.source_schedule.pk)*factor
