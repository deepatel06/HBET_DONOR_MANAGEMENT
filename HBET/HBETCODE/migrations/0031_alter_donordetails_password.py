# Generated by Django 4.2.2 on 2023-07-11 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HBETCODE', '0030_donordetails_delete_donor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donordetails',
            name='password',
            field=models.CharField(default='Hbet@123', max_length=50),
        ),
    ]