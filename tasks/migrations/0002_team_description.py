# Generated by Django 5.0.4 on 2024-04-27 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='description',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
