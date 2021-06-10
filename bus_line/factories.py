import factory
import random
from .models import BusLine


class BusLineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BusLine

    name = factory.Faker('name')
    code = factory.Faker('ean13')
