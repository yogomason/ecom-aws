# Generated by Django 3.0.6 on 2020-05-28 22:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0005_auto_20200528_1941'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
    ]
