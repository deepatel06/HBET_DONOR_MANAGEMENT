# Generated by Django 4.2.2 on 2023-07-06 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HBETCODE', '0007_donor_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donor_details',
            name='address1',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='donor_details',
            name='address2',
            field=models.CharField(max_length=1000),
        ),
    ]
