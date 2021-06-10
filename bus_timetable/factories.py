import factory
from .models import BusTimetable
from bus_pair.factories import BusPairFactory
from bus_line.factories import BusLineFactory

class BusTimetableFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BusTimetable

    bus_pair = factory.SubFactory(BusPairFactory)
    bus_line = factory.SubFactory(BusLineFactory)
    departure_at = factory.Faker('date_time')
    arrive_at = factory.Faker('date_time')