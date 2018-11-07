# Generated by Django 2.0.6 on 2018-11-07 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_flow', '0008_orders_list_openid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orders_list',
            old_name='order_detail',
            new_name='spec',
        ),
        migrations.RenameField(
            model_name='orders_list',
            old_name='ps',
            new_name='unit',
        ),
        migrations.RemoveField(
            model_name='orders_list',
            name='order_num',
        ),
        migrations.AddField(
            model_name='orders_list',
            name='order_qunantity',
            field=models.IntegerField(null=True),
        ),
    ]