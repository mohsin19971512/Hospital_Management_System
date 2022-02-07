# Generated by Django 4.0.1 on 2022-02-03 09:10

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0006_doctor_age_doctor_gender_patient_profile_age_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Prescription', models.CharField(max_length=1000)),
                ('symptoms', models.CharField(max_length=100)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created date')),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='prescription', to='hospital.doctor')),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='prescription', to='hospital.patient_profile')),
            ],
        ),
    ]