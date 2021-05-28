import factory
import random
from .models import BusLine


class BusLineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BusLine

    name = factory.Faker('name')
    code = random.randrange(10**0, 10**8)
