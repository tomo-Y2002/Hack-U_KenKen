from django.contrib import admin

from .models import Person,Record

#テスト用
admin.site.register(Person)
admin.site.register(Record)
