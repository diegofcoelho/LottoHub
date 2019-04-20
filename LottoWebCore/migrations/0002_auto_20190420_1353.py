# Generated by Django 2.2 on 2019-04-20 16:53

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('LottoWebCore', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='middleman',
            unique_together={('user', 'directory')},
        ),
        migrations.RemoveField(
            model_name='middleman',
            name='raffle',
        ),
    ]
