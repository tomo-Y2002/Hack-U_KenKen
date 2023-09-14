from django.urls import path
from . import views
urlpatterns=[
    path('', views.home, name="home"),

    path('manager_login/',views.manager_login,name='manager_login'),
    path('manager_logout/',views.manager_logout,name='manager_logout'),
    path('manager_register/',views.manager_register,name='manager_register'),

    path('realtime/',views.realtime,name="realtime"),

    path('person_register/',views.person_register,name="person_register"),

    path('person_list/',views.person_list,name='person_list'),
    path('person_record/<str:name>id=<str:id>/',views.person_record, name='person_record'),
    path('person_modify/<str:name>id=<str:id>/',views.person_modify,name='person_modify'),
    path('all_records/',views.all_records,name='all_records'),
    path('delete_modify_history/',views.delete_modify_history,name='delete_modify_history'),
    path('change_records/<str:id>',views.change_records,name='change_records'),
    path('add_records',views.add_records,name='add_records'),

]