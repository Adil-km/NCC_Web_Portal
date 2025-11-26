
from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard" ),
    path('assign-role/', views.assign_role_view, name="assign-role" ),
    path('create-group/', views.create_group_view, name="create-group" ),

]
