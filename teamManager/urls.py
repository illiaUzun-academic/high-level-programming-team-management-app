from django.urls import path

from . import views

urlpatterns = [
    path('team-list', views.team_list, name='team-list'),
    path('team-create', views.team_create, name='team-create'),
    path('team-update/<str:team_id>', views.team_update, name='team-update'),
    path('team-delete/<str:team_id>', views.team_delete, name='team-delete'),

    path('team-view/<str:team_id>', views.team_view, name='team-view'),
    path('employee-create/<str:team_id>', views.employee_create, name='employee-create'),
    path('employee-update/<str:employee_id>', views.employee_update, name='employee-update'),
    path('employee-delete/<str:employee_id>', views.employee_delete, name='employee-delete'),
]
