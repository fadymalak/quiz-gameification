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
from django.contrib import admin
from django.urls import path, reverse, resolve, include
from myapi.views.user_views import UserViewSet
from myapi.views.quiz_views import QuizViewSet
from myapi.views.courses_views import CourseViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views
from rest_framework_nested import routers
from badges.views import achievements , rules
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

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"quiz", QuizViewSet, basename="quiz")
router.register(r"course", CourseViewSet, basename="course")
router.register(r"achievement",achievements.AchievementViewSet)
achievement = routers.NestedSimpleRouter(router,r'achievement',lookup='achievement_level')
achievement.register(r'rules',rules.RulesViewSet,basename='achievement-level-rules')
urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/token/", jwt_views.TokenObtainPairView.as_view(), name="token_pair"),
    path(
        "auth/token/refresh/",
        jwt_views.TokenRefreshView.as_view(),
        name="token_pair_refresh",
    ),
       path(r'swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
# urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]
urlpatterns += router.urls
urlpatterns += achievement.urls
