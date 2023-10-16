# 启动django
import os
import sys
import django

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'day06.settings')
django.setup()  # 伪造让django启动

from web import models
from utils.encrypt import md5

models.Administrator.objects.create(username='root123', password=md5("root123"), mobile="1888888889")
