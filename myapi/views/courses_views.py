from rest_framework import serializers
from rest_framework.decorators import (
    authentication_classes,
    permission_classes,
    renderer_classes,
)
from rest_framework.viewsets import ModelViewSet
from ..models import Courses, User
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from ..serializers.course_serializers import CourseDetailSerializer, CourseSerializers
from django.db.models import Q, Value, F
from django.db.models.functions import Concat
from rest_framework.permissions import IsAuthenticated, AllowAny
from myapi.permissions import IsTeacher, IsEnrolled
from rest_framework.response import Response
from rest_framework import status


class CourseViewSet(ModelViewSet):
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    permission_classes = [
        ((IsEnrolled | IsTeacher) & IsAuthenticated),
    ]

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsTeacher, IsAuthenticated]
            return [permission() for permission in permission_classes]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.method == "GET":
            # return Course Details
            return CourseDetailSerializer
        return CourseSerializers

    def get_object(self):
        course_id = self.kwargs[self.lookup_field]
        return Courses.objects.get(id=course_id)

    def get_queryset(self):
        param = self.request.query_params
        search = param.get("search", 1)

        return Courses.objects.alias(
            oname=Concat(F("owner__first_name"), Value(" "), F("owner__last_name"))
        ).filter(
            Q(oname__contains=search)
            | Q(name__contains=search)
            | Q(owner__username__contains=search)
            # Q(id = search)
        )[
            :10
        ]

    def create(self, request):
        """'
        Create New Course
        set owner :param request.user.id
        """
        data = request.data.copy()
        # data = QueryDict(data)
        user = request.user
        data["owner"] = user.id
        serializer = CourseSerializers(data=data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        # else:
        # return Response(data=serializer.errors,status=status.HTTP_406_NOT_ACCEPTABLE)
