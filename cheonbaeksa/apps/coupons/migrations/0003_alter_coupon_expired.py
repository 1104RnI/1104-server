# Generated by Django 3.2.16 on 2024-06-17 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0002_insert_default_coupon_group_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='expired',
            field=models.DateTimeField(blank=True, null=True, verbose_name='만료 시간'),
        ),
    ]