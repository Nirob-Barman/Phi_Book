# Generated by Django 5.0.1 on 2024-01-26 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0002_userdetails'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='username',
            field=models.CharField(default='username', max_length=30, unique=True),
        ),
    ]
