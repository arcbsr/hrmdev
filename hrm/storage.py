from django.conf import settings
from storages.hrm.s3boto3 import S3Boto3Storage

"""
Use these classes in your settings.py file

# settings.py

DEFAULT_FILE_STORAGE = 'cookups.storage.MediaStorage'
STATICFILES_STORAGE = 'cookups.storage.StaticStorage'
STATICFILES_LOCATION='/path-to-static'
MEDIAFILES_LOCATION='/path-to-media'

"""


# class StaticStorage(S3Boto3Storage):
#     location = settings.STATICFILES_LOCATION


class MediaStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False
