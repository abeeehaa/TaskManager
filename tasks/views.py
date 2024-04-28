from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Team, TeamMember
from django.views.generic import ListView
from .models import Task
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, UpdateView, DeleteView
from django.views import View
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q

from django.http import JsonResponse
from datetime import datetime

def search_users(request):
    if 'q' in request.GET:
        query = request.GET.get('q')
        users = User.objects.filter(username__icontains=query)
    else:
        users = User.objects.none()
    return render(request, 'search_users.html', {'users': users})

# @login_required
# def create_team(request):
#     if request.method == 'POST':
#         team_name = request.POST.get('name')
#         team = Team.objects.create(name=team_name, lead=request.user)
#         team_member = TeamMember(user=request.user, team=team, role='lead')
#         team_member.save()
#         return render(request, 'my_teams.html')
#     return render(request, 'create_team.html')

class CreateTeamView(LoginRequiredMixin, View):
    template_name = 'create_team.html'

    def post(self, request):
        team_name = request.POST.get('name')
        team = Team.objects.create(name=team_name, lead=request.user)
        team_member = TeamMember(user=request.user, team=team, role='lead')
        team_member.save()
        return redirect('my_teams') 

    def get(self, request):
        return render(request, self.template_name)

@login_required
def add_member_to_team(request, team_id):
    team = Team.objects.get(id=team_id)
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.filter(username=username).first()
        if user:
            if TeamMember.objects.filter(user=user, team=team).exists():
                messages.error(request, f"{username} is already a member of the team.")
            else:
                team_member = TeamMember(user=user, team=team, role='member')
                team_member.save()
                messages.success(request, f"{username} added to the team successfully.")
            return redirect('team_details', pk=team_id)
    return render(request, 'add_member.html', {'team': team})

# @login_required
class Home(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'home.html'
    context_object_name = 'tasks'
    def get_queryset(self):
            return Task.objects.filter(assigned_to_user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_tasks'] = Task.objects.filter(assigned_to_user=self.request.user).count()
        context['priority_tasks'] = Task.objects.filter(assigned_to_user=self.request.user, priority='high').count()
        context['complete_tasks'] = Task.objects.filter(assigned_to_user=self.request.user, status='complete').count()
        context['incomplete_tasks'] = Task.objects.filter(assigned_to_user=self.request.user, status='incomplete').count()
        return context
    
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        status = self.kwargs.get('status')
        priority = self.kwargs.get('priority')
        if status == 'all':
            tasks = Task.objects.filter(Q(assigned_to_user=self.request.user) | Q(assigned_by=self.request.user))
            return tasks
        elif status == 'priority' and priority in ['high', 'medium', 'low']:
            return Task.objects.filter(priority=priority)
        elif status == 'complete':
            return Task.objects.filter(assigned_to_user=self.request.user, status='complete')
        elif status == 'incomplete':
            return Task.objects.filter(assigned_to_user=self.request.user, status='incomplete')
        elif status == 'date':
            date_str = self.request.GET.get('date')
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            return Task.objects.filter(assigned_to_user=self.request.user, due_date=date)
        else:
            return Task.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status'] = self.kwargs.get('status')
        return context

class MyTeamsListView(LoginRequiredMixin, ListView):
    template_name = 'my_teams.html'
    context_object_name = 'teams'

    def get_queryset(self):
        user = self.request.user
        teams_as_member = TeamMember.objects.filter(user=user).values_list('team', flat=True).distinct()
        teams = Team.objects.filter(pk__in=teams_as_member)
        return teams
    
    


class TeamDetailView(LoginRequiredMixin, DetailView):
    model = Team
    template_name = 'team_details.html'
    context_object_name = 'team'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = self.get_object()
        members = TeamMember.objects.filter(team=team)
        context['members'] = members
        return context



class TeamMembersView(View):
    def get(self, request, *args, **kwargs):
        team_id = kwargs.get('pk')  # Assumes that the team ID is passed as a URL parameter
        team = Team.objects.get(pk=team_id)
        members = TeamMember.objects.filter(team=team)
        res = []
        for member in members:
            res.append(
              {"id": member.id,
               "username": member.user.username,
               }  
            )
        # Serialize the member data
        members_data = list(members.values('id', 'team', 'user'))  # Modify fields as necessary
        return JsonResponse(res, safe=False)  # safe=False is needed to serialize a list

class AssignTaskView(LoginRequiredMixin, View):
    template_name = 'assign_task.html'

    def get(self, request):
        user = request.user
        teams = Team.objects.filter(lead=user)
        context = {
            'teams': teams
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        # team_id = request.POST.get('team')
        # team = Team.objects.get(id=team_id)
        # team_members = TeamMember.objects.filter(team=team)
        
        # Assuming Task model has fields: title, description, due_date, priority, status
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        priority = request.POST.get('priority')
        status = request.POST.get('status')

        # Create the task
        task = Task.objects.create(
            assigned_by=request.user,
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            status=status
        )

        # Assign the task to a team member
        assigned_member_id = request.POST.get('assigned_to_user')
        assigned_member = TeamMember.objects.get(id=assigned_member_id)
        task.assigned_to_user = assigned_member.user
        task.save()

        return redirect('task_list', status='all')
    

class UpdateTaskView(LoginRequiredMixin, View):
    template_name = 'update_task.html'

    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        teams = Team.objects.filter(lead=request.user)
        assigned_user_team = Team.objects.filter(teammember__user=task.assigned_to_user).first()
        team_members = TeamMember.objects.filter(team=assigned_user_team)

        context = {
            'task': task,
            'teams': teams,
            'team_members': team_members
        }
        return render(request, self.template_name, context)
    
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)

        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        priority = request.POST.get('priority')
        status = request.POST.get('status')

        task.title = title
        task.description = description
        task.due_date = due_date
        task.priority = priority
        task.status = status

        # Assign the task to a team member
        assigned_member_id = request.POST.get('assigned_to_user')
        assigned_member = TeamMember.objects.get(id=assigned_member_id)
        task.assigned_to_user = assigned_member.user

        task.save()

        return redirect('task_list', status='all')

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('task_list', kwargs={'status': 'all'})


class DeleteTeamView(LoginRequiredMixin, View):
    def post(self, request, team_id):
        team = get_object_or_404(Team, id=team_id)
        team.delete()
        return redirect('my_teams')