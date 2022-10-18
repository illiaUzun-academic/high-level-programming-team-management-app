from django.urls import path

from . import views

urlpatterns = [
    path('team-list', views.team_list, name='team-list'),
    path('team-create', views.team_create, name='team-create'),
    path('team-update/<str:team_id>', views.team_update, name='team-update'),
    path('team-delete/<str:team_id>', views.team_delete, name='team-delete')
]
