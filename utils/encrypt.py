import hashlib
from django.conf import settings


def md5(data_string):
    try:
        obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
        obj.update(data_string.encode('utf-8'))
        return obj.hexdigest()
    except AttributeError as e:
        print("data_string为空")
