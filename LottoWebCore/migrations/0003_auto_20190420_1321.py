# Generated by Django 2.2 on 2019-04-20 16:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LottoWebCore', '0002_auto_20190420_1314'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='middleman',
            unique_together={('id',)},
        ),
        migrations.RemoveField(
            model_name='middleman',
            name='directory',
        ),
        migrations.RemoveField(
            model_name='middleman',
            name='raffle',
        ),
    ]