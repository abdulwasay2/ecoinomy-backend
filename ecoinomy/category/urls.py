from django.urls import include, re_path
from rest_framework.routers import DefaultRouter
# from backendapp.routers import NestedDefaultRouter

from category import views


router = DefaultRouter()

router.register(r"", views.CategoryViewSet, basename='category')

urlpatterns = [
    re_path("", include(router.urls)),
]