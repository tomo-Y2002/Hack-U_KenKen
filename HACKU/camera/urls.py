from django.urls import path
from . import views

app_name = 'camera'
urlpatterns=[
    path('', views.index, name="index"),
    path('capture/', views.capture, name="capture"),
    path('test_flag/', views.test_flag, name="test_flag"),
    path('test_register/', views.test_register, name="test_register"),
    path('hoyou_register/',views.hoyou_register, name="hoyou_register"),
    path('ajax_recieve/', views.ajax_recieve, name="ajax_recieve"),
]