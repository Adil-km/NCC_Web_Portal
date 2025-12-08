
from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard" ),
    path('assign-role/', views.assign_group, name="assign-role" ),
    path('create-group/', views.create_group, name="create-group" ),
    path('cadet/', views.cadet, name="cadet" ),
    path('faculty/', views.faculty, name="faculty" ),
]
