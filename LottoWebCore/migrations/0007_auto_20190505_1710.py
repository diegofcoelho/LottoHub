# Generated by Django 2.2 on 2019-05-05 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LottoWebCore', '0006_auto_20190505_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='raffle',
            name='prizes',
            field=models.ManyToManyField(default=None, to='LottoWebCore.Prize'),
        ),
    ]