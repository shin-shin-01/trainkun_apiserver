import factory
from .models import BusTimetable
from busstop.factories import BusstopFactory


class BusTimetableFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BusTimetable

    departure_bus_stop = factory.SubFactory(BusstopFactory)
    arrival_bus_stop = factory.SubFactory(BusstopFactory)
