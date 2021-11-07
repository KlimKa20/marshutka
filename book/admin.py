from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Station)
admin.site.register(Car)
admin.site.register(Schedule)
admin.site.register(SeatChart)
admin.site.register(TypeSeat)
admin.site.register(Ticket)
