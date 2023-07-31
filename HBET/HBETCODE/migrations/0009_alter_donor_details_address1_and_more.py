# Generated by Django 4.2.2 on 2023-07-06 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HBETCODE', '0008_alter_donor_details_address1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donor_details',
            name='address1',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='donor_details',
            name='address2',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='donor_details',
            name='city',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='donor_details',
            name='first_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='donor_details',
            name='full_name',
            field=models.CharField(default='NA', max_length=200),
        ),
        migrations.AlterField(
            model_name='donor_details',
            name='last_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='donor_details',
            name='state',
            field=models.CharField(max_length=100),
        ),
    ]