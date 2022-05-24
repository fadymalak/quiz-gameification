from django.dispatch import receiver
from django.db.models.signals import post_save
from myapi.models import Answer


@receiver(signal=post_save,sender=Answer)
def add_variable(sender,instance,created,using,update_fields,**kwargs):
    print("[*] Start Signaling")
    print(sender)
    #for group_key
    group = type(instance.question.item).__name__ 

    print(created)
    print(kwargs['raw'])
    print(using)
    print(update_fields)
    # print(raw)
    
    

    
    print("[*] End Signaling")
    
