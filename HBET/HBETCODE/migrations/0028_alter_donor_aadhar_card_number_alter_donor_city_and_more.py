# Generated by Django 4.2.2 on 2023-07-06 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HBETCODE', '0027_alter_donor_password_alter_donor_spouse_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donor',
            name='aadhar_card_number',
            field=models.CharField(max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='donor',
            name='city',
            field=models.CharField(max_length=2),
        ),
        migrations.AlterField(
            model_name='donor',
            name='first_name',
            field=models.CharField(max_length=2),
        ),
        migrations.AlterField(
            model_name='donor',
            name='full_name',
            field=models.CharField(max_length=4),
        ),
        migrations.AlterField(
            model_name='donor',
            name='last_name',
            field=models.CharField(max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='donor',
            name='mobile_number1',
            field=models.CharField(max_length=1),
        ),
        migrations.AlterField(
            model_name='donor',
            name='mobile_number2',
            field=models.CharField(max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='donor',
            name='pan_card_number',
            field=models.CharField(max_length=1),
        ),
        migrations.AlterField(
            model_name='donor',
            name='password',
            field=models.CharField(max_length=1),
        ),
        migrations.AlterField(
            model_name='donor',
            name='spouse_name',
            field=models.CharField(max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='donor',
            name='state',
            field=models.CharField(max_length=2),
        ),
    ]
