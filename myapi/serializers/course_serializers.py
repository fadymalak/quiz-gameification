from rest_framework import serializers
from myapi.models import Courses


class CourseSerializers(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = ["owner", "name"]


class CourseDetailSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Courses
        exclude = ["id"]
