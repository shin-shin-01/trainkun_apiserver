import factory
from .models import BusPair
from busstop.factories import BusstopFactory


class BusPairFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BusPair

    departure_bus_stop = factory.SubFactory(BusstopFactory)
    arrival_bus_stop = factory.SubFactory(BusstopFactory)
