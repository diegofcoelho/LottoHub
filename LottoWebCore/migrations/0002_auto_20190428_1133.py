# Generated by Django 2.2 on 2019-04-28 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LottoWebCore', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentdirectory',
            name='acronym',
            field=models.CharField(default=None, max_length=12, verbose_name='Sigla do Centro'),
            preserve_default=False,
        ),
    ]