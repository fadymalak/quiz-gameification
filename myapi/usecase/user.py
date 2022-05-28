from typing import Union , List 
from myapi.services.user import UserService
from rest_framework.exceptions import ParseError 
from myapi.models import User
def user_update(user,**data):
    _check_fields(**data)
    user = UserService.update(user,**data)
    return user

def user_create(**data) -> User:
    _check_fields(**data)
    print("data ",str(data))
    user = UserService.create(**data)
    return user

def user_list(query:str) -> List[Union[User,None]]:
    queryset  = UserService.get_users_by_name(query['name'])
    users  = [ user for user in queryset ]
    return users

def _check_fields(**data) -> None:
    for i in data.keys():
        if i not in \
                ["username",'password',
                "last_name","first_name","bio","picture",'private']:
            raise ParseError(detail="Unsupported fields provided")
