# Generated by Django 2.2 on 2019-04-20 16:14

import LottoWebCore.methods
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LottoWebCore', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='middleman',
            name='id',
            field=models.CharField(default=LottoWebCore.methods.create_hash, max_length=100, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='middleman',
            unique_together={('id', 'directory', 'raffle')},
        ),
    ]