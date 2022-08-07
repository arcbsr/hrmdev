# Generated by Django 3.2 on 2022-03-18 18:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('degree', models.CharField(max_length=250)),
                ('graduate_date', models.DateField()),
                ('subject', models.CharField(max_length=250)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.RenameField(
            model_name='address',
            old_name='apt_no',
            new_name='house',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='house_no',
            new_name='road',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='street',
            new_name='state',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='area',
            new_name='zip',
        ),
        migrations.RenameField(
            model_name='employeeprofile',
            old_name='phone_number',
            new_name='phone',
        ),
        migrations.RenameField(
            model_name='employeeprofile',
            old_name='employee_type',
            new_name='profile_type',
        ),
        migrations.RenameField(
            model_name='employeeprofile',
            old_name='gender',
            new_name='sex',
        ),
        migrations.RemoveField(
            model_name='address',
            name='country',
        ),
        migrations.RemoveField(
            model_name='address',
            name='post_code',
        ),
        migrations.RemoveField(
            model_name='employeeprofile',
            name='fb_link',
        ),
        migrations.RemoveField(
            model_name='employeeprofile',
            name='linked_in_link',
        ),
        migrations.RemoveField(
            model_name='employeeprofile',
            name='marital_status',
        ),
        migrations.RemoveField(
            model_name='employeeprofile',
            name='profile_picture',
        ),
        migrations.RemoveField(
            model_name='employeeprofile',
            name='twitter_link',
        ),
        migrations.AddField(
            model_name='address',
            name='address_type',
            field=models.IntegerField(choices=[(1, 'Home'), (2, 'Permanent')], default=1),
        ),
        migrations.AddField(
            model_name='address',
            name='village',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='company',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='emergency_phone',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='joining_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='passport_or_nid',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='remaining_leave',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='role',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='total_leave',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='education',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='api.education'),
        ),
    ]
