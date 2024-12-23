# Generated by Django 5.0.6 on 2024-12-23 07:23

import backend.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_alter_bulkstudentregistration_payment_proof_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bulkstudentregistration',
            name='reg_num',
            field=models.CharField(default=backend.models.generate_tsreg_num, max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='guru',
            name='profile_photo',
            field=models.ImageField(blank=True, null=True, upload_to='guru_profile/'),
        ),
        migrations.AlterField(
            model_name='gurustudentassociation',
            name='group_registered_students',
            field=models.ManyToManyField(blank=True, null=True, related_name='students', to='backend.bulkstudentregistration'),
        ),
        migrations.AlterField(
            model_name='gurustudentassociation',
            name='students',
            field=models.ManyToManyField(blank=True, null=True, related_name='students', to='backend.student'),
        ),
    ]