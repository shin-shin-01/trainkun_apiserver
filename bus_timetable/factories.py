import factory
from factory.faker import faker
from datetime import timedelta, timezone
from .models import BusTimetable
from bus_pair.factories import BusPairFactory
from bus_line.factories import BusLineFactory

FAKE = faker.Faker()
JST = timezone(timedelta(hours=+9), 'JST')


class BusTimetableFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BusTimetable

    bus_pair = factory.SubFactory(BusPairFactory)
    bus_line = factory.SubFactory(BusLineFactory)
    departure_at = FAKE.date_time(tzinfo=JST).isoformat()
    arrive_at = FAKE.date_time(tzinfo=JST).isoformat()
