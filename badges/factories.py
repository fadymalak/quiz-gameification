import factory
from myapi.tests.factories import UserFactory
from badges.models import Achievement , AchievementLevel

class AchievementFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda id:f"Achievement {id}")
    owner = factory.SubFactory(UserFactory)
    class Meta:
        model = Achievement

class AchievementLevelFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda id:f"Achievement Level {id}")
    owner = factory.SubFactory(UserFactory)
    achievement = factory.SubFactory(AchievementFactory)
    parent = None

    class Meta:
        model = AchievementLevel

        
    