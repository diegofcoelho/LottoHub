# Generated by Django 2.2 on 2019-04-25 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LottoWebCore', '0008_auto_20190420_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='raffle',
            name='prizes',
            field=models.CharField(max_length=500, null=True, verbose_name='Premiação'),
        ),
    ]
