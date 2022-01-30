from rest_framework import serializers
from ..models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = "__all__"
        fields = ["first_name","last_name","username","email"]
        extra_kwargs = {
            "password":{
                "write_only":True
                }
            }

    def create(self,validated_data):
        return User.objects.create_user(**validated_data)
        

class UserDetailsSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="full_name",read_only=True)
    class Meta:
        model = User
        fields = "__all__"
        depth = 1
        extra_kwargs = {
            "password":{
                "write_only":True
            }
        }   