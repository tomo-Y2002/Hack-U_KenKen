from django.urls import path
from . import views
urlpatterns=[
    path('', views.home, name="home"),

    path('realtime/',views.realtime,name="realtime"),

    path('person_register',views.person_register,name="person_register"),
]