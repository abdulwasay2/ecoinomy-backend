from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import CustomRegisterView


urlpatterns = [
    path('registration/', CustomRegisterView.as_view(), name='rest_register'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
