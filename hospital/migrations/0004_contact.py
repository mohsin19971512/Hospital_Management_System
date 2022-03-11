# Generated by Django 4.0.1 on 2022-03-10 17:45

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0003_surgery'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('created', models.DateTimeField(auto_created=True, blank=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('phone_number', models.CharField(max_length=12, verbose_name='Phone Number')),
                ('subject', models.TextField(verbose_name=' Message')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]