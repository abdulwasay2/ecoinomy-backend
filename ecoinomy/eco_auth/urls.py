from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from dj_rest_auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView
from dj_rest_auth.jwt_auth import get_refresh_view

from .views import CustomRegisterView, VerifyOTPView


urlpatterns = [
    path('user_login/', CustomRegisterView.as_view(), name='user-login'),
    path('user_verify_otp/', VerifyOTPView.as_view(), name='verify-login-otp'),
    path('admin_login/', LoginView.as_view(), name='admin-login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password/reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('token_refresh/', get_refresh_view().as_view(), name="token_refresh"),
]
