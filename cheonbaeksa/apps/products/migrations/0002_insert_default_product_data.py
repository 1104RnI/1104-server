# Django
from django.db import migrations


# Main Section
def forwards_insert_default_data(apps, schema_editor):
    Product = apps.get_model('products', 'Product')

    data_list = [
        {
            'title': 'Quant',
            'price': '7500000',
            'subscription_price': '50000',
            'description': ''
        },
    ]

    for data in data_list:
        Product.objects.create(title=data['title'],
                               price=data['price'],
                               subscription_price=data['subscription_price'],
                               description=data['description'])

    return True


def reverse_insert_default_data(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            code=forwards_insert_default_data,
            reverse_code=reverse_insert_default_data,
        ),
    ]
