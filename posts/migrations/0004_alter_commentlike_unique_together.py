# Generated by Django 4.2 on 2024-09-13 11:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_alter_commentlike_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='commentlike',
            unique_together=set(),
        ),
    ]
