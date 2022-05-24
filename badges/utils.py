


from myapi.models import User


def check_staff(user:User,obj,action) -> bool:
    #check if user has access rights to perform action to obj 
    return user.is_staff