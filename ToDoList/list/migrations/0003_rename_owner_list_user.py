# Generated by Django 4.1.7 on 2023-04-07 22:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('list', '0002_list_date_created_list_date_modified_list_owner_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='list',
            old_name='owner',
            new_name='user',
        ),
    ]
