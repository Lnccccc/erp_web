# Generated by Django 2.0.6 on 2018-12-18 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='dept',
            field=models.CharField(choices=[('总经理', '总经理'), ('厂长', '厂长'), ('生产主管', '生产主管'), ('仓管', '仓管'), ('空', '空')], default='总经理', max_length=200, null=True),
        ),
    ]
