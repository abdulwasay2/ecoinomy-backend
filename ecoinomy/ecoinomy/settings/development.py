from ecoinomy.settings.common import *
from ecoinomy.settings import env

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')
OTP_SECRET_KEY = env('OTP_SECRET_KEY')
PASSWORD_RESET_OTP_SECRET = env('PASSWORD_RESET_OTP_SECRET')

CORS_ALLOWED_ORIGINS = ["http://127.0.0.1:8000", "http://ec2-51-20-128-52.eu-north-1.compute.amazonaws.com"]

# aws settings
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_DEFAULT_ACL = None
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
# s3 static settings
# STATIC_LOCATION = 'static'
# STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
# STATICFILES_STORAGE = 'ecoinomy.storage_backends.StaticStorage'
# s3 public media settings
PUBLIC_MEDIA_LOCATION = 'media'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
DEFAULT_FILE_STORAGE = 'ecoinomy.storage_backends.PublicMediaStorage'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

# Twilio Settings
TWILIO_ACCOUNT_SID=env("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN=env("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER=env("TWILIO_PHONE_NUMBER")