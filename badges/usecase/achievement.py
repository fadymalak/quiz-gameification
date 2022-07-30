from badges.models import AchievementLevel
from badges.services.achievement import AchievementService , AchievementLevelService

def get_achievement(ach_id:int):
    return AchievementService.get_by_id(ach_id)

def create_achievement(name,owner):
    return AchievementService.create(name,owner)

def update_achievement(name:str,ach_id:int) :
    achievement = AchievementService.get_by_id(ach_id=ach_id)
    achievement.name = name
    achievement.save()
    return achievement

def get_achievement_level(ach_l_id:int):
    achievement_level = AchievementLevelService.get_by_id(ach_l_id)
    return achievement_level

def create_achievement_level(ach_id,data,owner):
    achievement = AchievementService.get_by_id(ach_id)
    data = {"achievement":achievement,"name":data['name'],"owner":owner}
    achievement_level = AchievementLevelService.create(data)
    return achievement_level

def update_achievement_level(ach_l_id,data):
    achievement_level = AchievementLevelService.get_by_id(ach_l_id)

    for k,v in data.items():
        if getattr(achievement_level,k) != v:
            if k in ["parent","achievement"]:
                #assign foregin key id instead of object by using parent_id & achievement_id
                setattr(achievement_level,k+"_id",v)
            else:
                setattr(achievement_level,k,v)

    achievement_level.save()
    return achievement_level