from ecoinomy.settings.common import *
from ecoinomy.settings import env

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')
OTP_SECRET_KEY = env('OTP_SECRET_KEY')
PASSWORD_RESET_OTP_SECRET = env('PASSWORD_RESET_OTP_SECRET')