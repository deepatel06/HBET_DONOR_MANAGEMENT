# Generated by Django 4.2.2 on 2023-07-06 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HBETCODE', '0006_admin_details_email_admin_details_full_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='donor_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=1000)),
                ('last_name', models.CharField(max_length=1000, null=True)),
                ('full_name', models.CharField(default='NA', max_length=2000)),
                ('email', models.EmailField(default='NA', max_length=254)),
                ('password', models.CharField(max_length=128)),
                ('date_of_birth', models.DateField()),
                ('date_of_marriage', models.DateField(null=True)),
                ('spouse_name', models.CharField(max_length=1000, null=True)),
                ('address1', models.CharField(max_length=10000)),
                ('address2', models.CharField(max_length=10000)),
                ('date_of_registration', models.DateField()),
                ('city', models.CharField(max_length=1000)),
                ('state', models.CharField(max_length=1000)),
                ('pin_code', models.CharField(max_length=6)),
                ('mobile_number1', models.CharField(max_length=12)),
                ('mobile_number2', models.CharField(max_length=12, null=True)),
                ('aadhar_card_number', models.IntegerField(null=True)),
                ('pan_card_number', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'donor_details',
            },
        ),
    ]