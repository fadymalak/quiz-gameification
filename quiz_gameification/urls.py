"""quiz_gameification URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from cgitb import lookup
from django.contrib import admin
from django.db import router
from django.urls import path, reverse, resolve, include , re_path
from myapi.views.user_views import UserViewSet
from myapi.views.quiz_views import   QuizViewSet , AnswerViewset
from myapi.views.courses_views import CourseViewSet
from myapi.views.question_views import QuestionViewset
from rest_framework_simplejwt import views as jwt_views
from rest_framework_nested import routers
from badges.views import achievements , rules
from badges.views.rules import RulesViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)
course = routers.DefaultRouter()
course.register(r"course",CourseViewSet,basename="courses")
quiz = routers.NestedSimpleRouter(course,r'course',lookup="course")
quiz.register(r'quiz',QuizViewSet,basename='quizes')
answer =routers.NestedSimpleRouter(quiz,r'quiz',lookup="quiz")
answer.register(r'answer',AnswerViewset,basename="answer")
answer.register(r'question',QuestionViewset,basename="qusetion")

achievement = routers.DefaultRouter()
achievement.register(r"achievement",achievements.AchievementViewSet,basename='achievement')
level = routers.NestedSimpleRouter(achievement, r'achievement', lookup='achievement')
level.register(r"level",achievements.AchievementLevelViewSet,basename="achievement_level")
rules = routers.NestedSimpleRouter(level, r'level', lookup='achievement_level')
rules.register('rules',RulesViewSet,basename="rules")

urlpatterns = [
    path("admin/", admin.site.urls),
    # re_path(r"^course/(?P<pk>[0-9]*)[\/]*$",CourseViewSet.as_view({v:v for v in ["get","post","patch","delete"]}),name="course-view"),
    # re_path(r"^course/(?P<course_id>[0-9]+)/quiz/(?P<pk>[0-9]*)[\/]*$",QuizViewSet.as_view({"post":"post","get":"get","get":"list"}),name='quiz-detials'),
    # re_path(r"^course/(?P<course_id>[0-9]+)/quiz/(?P<quiz_id>[0-9]+)/question/(?P<pk>[0-9]*)[\/]*$",QuestionViewset.as_view({"post":"post","get":"get"}),name='question-detials'),
    # re_path(r"^course/(?P<course_id>[0-9]+)/quiz/(?P<quiz_id>[0-9]+)/answer/(?P<pk>[0-9]*)[\/]*$",AnswerViewset.as_view({"post":"post","get":"get","get":"list"}),name='quiz-detials'),
    path("user/",UserViewSet.as_view({"post":"create"}),name='quiz-detials'),
    path("user/<int:pk>/",UserViewSet.as_view({'get':'retrieve','patch':'partial_update','delete':'destroy'}),name='quiz-detials'),
    path("auth/token/", jwt_views.TokenObtainPairView.as_view(), name="token_pair"),
    path(
        "auth/token/refresh/",
        jwt_views.TokenRefreshView.as_view(),
        name="token_pair_refresh",
    ),
       path(r'swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
path("",include(achievement.urls)),
path("",include(rules.urls))
]
# urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]
# urlpatterns += router.urls
urlpatterns += achievement.urls
urlpatterns += level.urls
urlpatterns += rules.urls
urlpatterns += course.urls
urlpatterns += quiz.urls
urlpatterns += answer.urls


