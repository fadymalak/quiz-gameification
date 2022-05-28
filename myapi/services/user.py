


from myapi.models import User
from django.db.models import Subquery
from django.db.models import Q
from typing import List
from django.db.models import QuerySet
class UserService:
    def get_users_by_name(name:str)-> QuerySet[User]:
        users = User.objects.filter(Q(username__contains=name)|Q(last_name__contains=name)|\
            Q(first_name__contains=name)|Q(bio__contains=name)).all()
        return users
        
    def get_by_id(id):
        user = User.objects.get(id=id)
        return user
    
    def create(**data) -> User :
        return User.objects.create_user(**data)
        
    def update(user:User,**data:dict) -> User:
        
        for k,v in data.items():
            if k == "password":
                user.set_password(v)
            else:
                value = getattr(user,k)
                if value != v :
                    setattr(user,k,v)
        
        user.save()
        return user

    