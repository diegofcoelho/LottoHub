# Generated by Django 2.2 on 2019-04-20 17:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LottoWebCore', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='directory',
        ),
    ]