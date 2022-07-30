from re import A
from badges.models import Achievement , AchievementLevel
from django.db.models import QuerySet
from django.core.exceptions import ValidationError

from myapi.models import User

class AchievementService():
    def get_by_id(ach_id:int):
        return Achievement.objects.prefetch_related("achievement_levels").get(id=ach_id)

    def get_by_name(name:str):
        return Achievement.objects.prefetch_related("achievement_levels").get(name=name)

    def create(name:str,owner:User):
        return Achievement.objects.get_or_create(name=name,defaults={"owner":owner,"name":name})

    def delete(ach_id:int):
        achivement = Achievement.objects.get(id=ach_id)
        achivement.deleted=1
        achivement.save()
        return achivement


class AchievementLevelService():
    def get_by_id(ach_l_id:int) -> AchievementLevel:
        return AchievementLevel.objects.get(id=ach_l_id)

    def get_by_name(name:str) -> AchievementLevel:
        return AchievementLevel.objects.get(name=name)
    
    def get_by_achievement_name(ach_name:str) -> QuerySet[AchievementLevel]:
        return AchievementLevel.objects.filter(achievement__name=ach_name).all()

    def create(data:dict) -> AchievementLevel:
        name = data.get("name",None)
        if name is None :
            raise ValidationError(message='name should be included')
        return AchievementLevel.objects.get_or_create(name=name,defaults=data)
