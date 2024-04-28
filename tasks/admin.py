from django.contrib import admin
from tasks.models import Task, Team, TeamMember


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title','description', 'due_date', 'assigned_by', 'status', 'priority', 'progress', 'assigned_to_user')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name','lead')


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('id','user','team', 'role')