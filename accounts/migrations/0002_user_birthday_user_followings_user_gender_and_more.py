# Generated by Django 4.2 on 2024-09-16 16:02

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="birthday",
            field=models.DateField(default="2000-01-01"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="user",
            name="followings",
            field=models.ManyToManyField(
                blank=True, related_name="followers", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="gender",
            field=models.CharField(
                choices=[("M", "Male"), ("F", "Female")], default="F", max_length=10
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(blank=True, max_length=254, unique=True),
        ),
    ]
