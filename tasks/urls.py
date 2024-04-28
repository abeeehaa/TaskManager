from django.urls import path
# from tasks.views import Home, search_users, create_team, add_member_to_team, TaskListView, MyTeamsListView, TeamDetailView
from tasks.views import *
urlpatterns = [
    path('search_users/', search_users, name='search_users'),
    path('create_team/', CreateTeamView.as_view(), name='create_team'),
    path('team/<int:team_id>/add_member/', add_member_to_team, name='add_member_to_team'),
    path('', Home.as_view(), name='home'),
    path('tasks/<str:status>/', TaskListView.as_view(), name='task_list'),
    path('my-teams/', MyTeamsListView.as_view(), name='my_teams'),
    path('team/<int:pk>/', TeamDetailView.as_view(), name='team_details'),
    path('team_members/<int:pk>/', TeamMembersView.as_view(), name='team_members'),
    path('assign_task/', AssignTaskView.as_view(), name='assign_task'),
]
