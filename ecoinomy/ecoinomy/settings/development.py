from ecoinomy.settings.common import *
from ecoinomy.settings import env

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')
OTP_SECRET_KEY = env('OTP_SECRET_KEY')
PASSWORD_RESET_OTP_SECRET = env('PASSWORD_RESET_OTP_SECRET')

CORS_ALLOWED_ORIGINS = ["http://127.0.0.1:8000", "http://ec2-51-20-128-52.eu-north-1.compute.amazonaws.com"]