# Generated by Django 4.0.1 on 2022-02-20 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0002_remove_doctor_details_remove_doctor_facebook_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='doctor',
            old_name='mobile',
            new_name='phone_number',
        ),
    ]