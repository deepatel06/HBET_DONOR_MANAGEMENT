# Generated by Django 4.2.2 on 2023-07-06 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HBETCODE', '0019_alter_donor_details_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin_details',
            name='first_name',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='admin_details',
            name='full_name',
            field=models.TextField(default='NA'),
        ),
        migrations.AlterField(
            model_name='admin_details',
            name='last_name',
            field=models.TextField(),
        ),
    ]
