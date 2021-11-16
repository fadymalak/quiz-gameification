from rest_framework import serializers
from ..models import *

class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='full_name',read_only=True)
    class Meta:
        model = User
        # fields = "__all__"
        exclude = ['first_name',"last_name","password",'id']
        extra_kwargs = {"password":{"write_only":True}}