import factory
from factory.django import DjangoModelFactory

from network.models import NetworkNode, Product


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda n: f"Product{n}")
    model = factory.Sequence(lambda n: f"M{n}")
    release_date = "2024-01-01"


class NetworkNodeFactory(DjangoModelFactory):
    class Meta:
        model = NetworkNode

    name = factory.Sequence(lambda n: f"Node{n}")
    email = factory.LazyAttribute(lambda o: f"{o.name.lower()}@ex.com")
    country = "RU"
    city = "Москва"
    street = "Ленина"
    house = "1"
    supplier = None
