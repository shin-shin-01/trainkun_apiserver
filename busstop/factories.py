import factory
import random
from .models import Busstop


class BusstopFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Busstop

    name = factory.Faker('name')
    code = random.randrange(10**0,10**8)
