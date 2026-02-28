# check_db.py
import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hello_project.settings")
django.setup()

from django.db import connections

db_conn = connections['default']
c = db_conn.cursor()
print("База подключена!")
