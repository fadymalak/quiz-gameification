import functools

USER_ID = 1
GROUP_ID =1
OTHER = 1
def update(t=0):
    global USER_ID 
    global GROUP_ID 
    global OTHER
    if t == "g":
        GROUP_ID +=1
        return GROUP_ID
    elif t == "u":
        USER_ID +=1
        return USER_ID
    else:
        OTHER +=1
        return OTHER


def rgetattr(obj, attr, *args):
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)
    return functools.reduce(_getattr, [obj] + attr.split('.'))

def gen_quiz_data(*args,**kwargs):
    result = {}
    for k ,v in kwargs.items():
        result[k] = v
    return result


