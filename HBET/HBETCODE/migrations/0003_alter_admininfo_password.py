# Generated by Django 4.2.2 on 2023-06-27 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HBETCODE', '0002_admininfo_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admininfo',
            name='password',
            field=models.CharField(max_length=10),
        ),
    ]
