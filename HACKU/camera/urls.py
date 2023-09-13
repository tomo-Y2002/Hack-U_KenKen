from django.urls import path
from . import views

app_name = 'camera'
urlpatterns=[
    path('', views.index, name="index"),
    path('capture/', views.capture, name="capture"),
    path('test_flag/', views.test_flag, name="test_flag"),
    path('test_register', views.test_register, name="test_register")
]