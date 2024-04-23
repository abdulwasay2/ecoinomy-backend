from django.urls import include, re_path
from rest_framework.routers import DefaultRouter
# from backendapp.routers import NestedDefaultRouter

from user import views


router = DefaultRouter()

router.register(r"", views.UserViewSet, basename='users')
router.register(r"profile", views.ProfileViewSet, basename="profile")

urlpatterns = [
    re_path("", include(router.urls)),
]