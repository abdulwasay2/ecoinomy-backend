from ecoinomy.settings.common import *
from ecoinomy.settings import env

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')