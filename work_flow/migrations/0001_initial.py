# Generated by Django 2.0.6 on 2018-11-14 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='charge_person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_cd', models.CharField(max_length=200)),
                ('person_nam', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='order_stat',
            fields=[
                ('stat_cd', models.IntegerField(primary_key=True, serialize=False)),
                ('stat_nam', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='orders_list',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('openid', models.CharField(max_length=256, null=True)),
                ('user_name', models.CharField(max_length=200, null=True)),
                ('uuid', models.CharField(max_length=200, null=True)),
                ('client', models.CharField(max_length=200, null=True)),
                ('order_time', models.DateField()),
                ('sub_time', models.DateField()),
                ('order_quantity', models.IntegerField(null=True)),
                ('spec', models.CharField(max_length=200, null=True)),
                ('unit', models.CharField(max_length=200)),
                ('order_status', models.IntegerField()),
                ('person_incharge', models.CharField(max_length=100)),
                ('company', models.CharField(max_length=256, null=True)),
                ('requirement', models.CharField(default='暂无', max_length=256, null=True)),
                ('remark', models.CharField(default='暂无', max_length=256, null=True)),
                ('next_node', models.CharField(default='暂无', max_length=256, null=True)),
            ],
        ),
    ]
