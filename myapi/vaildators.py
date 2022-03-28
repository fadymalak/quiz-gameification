from django.core.exceptions import ValidationError


def vaild_name(val):
    if len(val) <= 2:
        raise ValidationError("Error Vaildatiors.py")
