# Generated by Django 4.2.2 on 2023-07-06 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HBETCODE', '0009_alter_donor_details_address1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donor_details',
            name='spouse_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]