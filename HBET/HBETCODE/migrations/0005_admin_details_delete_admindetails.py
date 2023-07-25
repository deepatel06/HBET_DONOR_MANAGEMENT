# Generated by Django 4.2.2 on 2023-06-27 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HBETCODE', '0004_rename_admininfo_admindetails'),
    ]

    operations = [
        migrations.CreateModel(
            name='admin_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=10)),
                ('address', models.TextField()),
            ],
        ),
        migrations.DeleteModel(
            name='admindetails',
        ),
    ]
