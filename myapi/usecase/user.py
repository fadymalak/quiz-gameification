from typing import Optional
from myapi.services.user import UserService
from rest_framework.exceptions import ParseError 
from myapi.models import User
def user_update(user,**data):
    _check_fields(**data)
    user = UserService.update(user,**data)
    return user

def create_user(**data) -> User:
    _check_fields(**data)
    print("data ",str(data))
    user = UserService.create(**data)
    return user


def _check_fields(**data) -> Optional[None]:
    for i in data.keys():
        if i not in \
                ["username",'password',
                "last_name","first_name","bio","picture",'private']:
            raise ParseError(detail="Unsupported fields provided")
