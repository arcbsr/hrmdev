# Generated by Django 3.2 on 2022-03-05 07:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apt_no', models.CharField(blank=True, max_length=255, null=True)),
                ('house_no', models.CharField(blank=True, max_length=255, null=True)),
                ('street', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('area', models.CharField(blank=True, max_length=50, null=True)),
                ('post_code', models.CharField(blank=True, max_length=10, null=True)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('head_of_department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='departments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_number', models.CharField(max_length=100)),
                ('employee_type', models.CharField(choices=[('general', 'general'), ('manager', 'manager'), ('hr', 'hr')], default='general', max_length=20)),
                ('name', models.CharField(max_length=255, null=True)),
                ('birth_date', models.DateField()),
                ('gender', models.CharField(choices=[('male', 'male'), ('female', 'female')], default='male', max_length=20)),
                ('marital_status', models.CharField(choices=[('single', 'single'), ('married', 'married')], default='single', max_length=20)),
                ('nationality', django_countries.fields.CountryField(max_length=2)),
                ('phone_number', models.CharField(max_length=20, null=True, unique=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='')),
                ('fb_link', models.URLField(blank=True, null=True)),
                ('twitter_link', models.URLField(blank=True, null=True)),
                ('linked_in_link', models.URLField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='api.address')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employees', to='api.department')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
