# Generated by Django 5.0.7 on 2024-07-12 11:34

import django.core.validators
import django.db.models.deletion
import isko.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser status')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('applicant_id', models.AutoField(primary_key=True, serialize=False)),
                ('applicant_name', models.CharField(max_length=80)),
                ('age', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(99), django.core.validators.MinValueValidator(1)])),
                ('sex', models.CharField(max_length=1, validators=[isko.models.validate_sex])),
                ('status', models.CharField(max_length=2, validators=[isko.models.validate_status])),
                ('religion', models.CharField(max_length=45)),
                ('citizenship', models.CharField(max_length=45)),
                ('birthday', models.DateField()),
                ('birthplace', models.CharField(max_length=45)),
                ('telephone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('mobile_number', models.CharField(max_length=15)),
                ('email_address', models.EmailField(max_length=45)),
                ('home_address', models.CharField(max_length=100)),
                ('highschool_name', models.CharField(max_length=45)),
                ('highschool_address', models.CharField(max_length=100)),
                ('highest_year', models.CharField(max_length=10, validators=[isko.models.validate_highest_year])),
                ('gwa', models.DecimalField(decimal_places=2, max_digits=2)),
                ('graduation_date', models.DateField()),
                ('father_status', models.CharField(max_length=1, validators=[isko.models.validate_parent_status])),
                ('father_name', models.CharField(max_length=80)),
                ('father_address', models.CharField(max_length=100)),
                ('father_occupation', models.CharField(max_length=30)),
                ('father_education', models.CharField(max_length=25)),
                ('mother_status', models.CharField(max_length=1, validators=[isko.models.validate_parent_status])),
                ('mother_name', models.CharField(max_length=80)),
                ('mother_address', models.CharField(max_length=100)),
                ('mother_occupation', models.CharField(max_length=30)),
                ('mother_education', models.CharField(max_length=25)),
                ('gross_income', models.DecimalField(decimal_places=2, max_digits=9)),
                ('no_of_children', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(99), django.core.validators.MinValueValidator(0)])),
                ('school_enroll', models.CharField(max_length=50)),
                ('first_choice', models.CharField(max_length=50)),
                ('second_choice', models.CharField(max_length=50)),
                ('third_choice', models.CharField(max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Honors',
            fields=[
                ('honors_id', models.AutoField(primary_key=True, serialize=False)),
                ('honors_received', models.CharField(max_length=45)),
                ('honors_school', models.CharField(max_length=70)),
                ('honors_date', models.DateField()),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='isko.applicant')),
            ],
        ),
        migrations.CreateModel(
            name='Siblings',
            fields=[
                ('sibling_id', models.AutoField(primary_key=True, serialize=False)),
                ('sibling_name', models.CharField(blank=True, max_length=50, null=True)),
                ('sibling_scholarship', models.CharField(blank=True, max_length=45, null=True)),
                ('sibling_age', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(999), django.core.validators.MinValueValidator(1)])),
                ('sibling_course_year', models.CharField(blank=True, max_length=45, null=True)),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='isko.applicant')),
            ],
        ),
    ]
