# Django
from django.db import migrations


# Main Section
def forwards_insert_default_data(apps, schema_editor):
    CouponGroup = apps.get_model('coupons', 'CouponGroup')

    data_list = [
        {
            'title': '커스텀',
            'discount_percentage': None,
            'valid_days': 10,
        },
        {
            'title': '사전 예약',
            'discount_percentage': 10,
            'valid_days': 10,
        },
    ]

    for data in data_list:
        CouponGroup.objects.create(title=data['title'],
                                   discount_percentage=data['discount_percentage'],
                                   valid_days=data['valid_days'])

    return True


def reverse_insert_default_data(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('coupons', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            code=forwards_insert_default_data,
            reverse_code=reverse_insert_default_data,
        ),
    ]
