from django.dispatch import receiver
from django.db.models.signals import post_delete
from myapi.models2 import Question

@receiver(post_delete,sender=Question)
def delete_item_object(sender,instance,using,**kwargs):
    instance.item.delete()
    return True