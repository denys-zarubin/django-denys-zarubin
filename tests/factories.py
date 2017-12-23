import factory
from accounts import models


class TeamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Team

    name = factory.Sequence(lambda n: "Team %03d" % n)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User

    team = factory.SubFactory(TeamFactory)
    email = factory.Sequence(lambda n: "john%03d@snow.com" % n)
    first_name = factory.Sequence(lambda n: "John %03d" % n)
    last_name = factory.Sequence(lambda n: "Snow %03d" % n)
