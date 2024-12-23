# Generated by Django 5.0.6 on 2024-12-22 15:07

import backend.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_alter_customuser_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gurustudentassociation',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='students', to='backend.student'),
        ),
        migrations.AlterField(
            model_name='student',
            name='payment_proof',
            field=models.ImageField(upload_to='media/inv_proof'),
        ),
        migrations.CreateModel(
            name='BulkStudentRegistration',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('reg_num', models.CharField(default=backend.models.generate_student_reg_num, max_length=20, unique=True)),
                ('payment_ref_no', models.CharField(max_length=100)),
                ('payment_proof', models.ImageField(upload_to='media/bulk_proof')),
                ('guru', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.guru')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'bulk_registration',
            },
        ),
        migrations.AddField(
            model_name='gurustudentassociation',
            name='group_registered_students',
            field=models.ManyToManyField(blank=True, related_name='students', to='backend.bulkstudentregistration'),
        ),
    ]
