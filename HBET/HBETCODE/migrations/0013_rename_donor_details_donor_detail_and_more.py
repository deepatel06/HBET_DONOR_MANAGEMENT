# Generated by Django 4.2.2 on 2023-07-06 10:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HBETCODE', '0012_alter_donor_details_city_alter_donor_details_state'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='donor_details',
            new_name='donor_detail',
        ),
        migrations.AlterModelTable(
            name='donor_detail',
            table='donor_detail',
        ),
    ]
