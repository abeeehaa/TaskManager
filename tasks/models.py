from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    STATUS_CHOICES = (
        ('incomplete', 'Incomplete'),
        ('complete', 'Complete'),
        ('in_progress', 'In Progress'),
        ('to_do', 'To Do'),


    )
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    )
    # Existing fields
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='incomplete')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='low')
    progress = models.CharField(max_length=250, null=True, blank=True)
    assigned_to_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title


class Team(models.Model):
    name = models.CharField(max_length=100)
    lead = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lead_teams', null=True, blank=True)
    description = models.CharField(max_length=250, null=True, blank=True)
    def __str__(self):
        return self.name

class TeamMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    role_choices = [
        ('lead', 'Team Lead'),
        ('member', 'Team Member'),
    ]
    role = models.CharField(max_length=10, choices=role_choices, default='member')