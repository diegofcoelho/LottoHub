# Generated by Django 2.2 on 2019-04-20 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LottoWebCore', '0004_auto_20190420_1325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='email',
            field=models.CharField(max_length=500, null=True, verbose_name='E-mail'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='name',
            field=models.CharField(max_length=500, null=True, verbose_name='Comprador'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='phone',
            field=models.CharField(max_length=500, null=True, verbose_name='Telefone'),
        ),
    ]
