from django.db import models

class admin_details(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    full_name = models.CharField(max_length=200,default="NA")
    email = models.EmailField(default='NA')
    password = models.CharField(max_length=10)
    address = models.TextField()

class DonorDetails(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    full_name = models.CharField(max_length=40)
    dob = models.DateField()
    dom = models.CharField(max_length=255, null=True, blank=True)
    spouse_name = models.CharField(max_length=255, null=True, blank=True)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    dor = models.DateField()
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    pin_code = models.CharField(max_length=6)
    mobile2 = models.CharField(max_length=20, null=True, blank=True)
    mobile1 = models.CharField(max_length=20)
    aadhar_card = models.BigIntegerField(null=True, blank=True)
    pan_card = models.CharField(max_length=10)
    email = models.EmailField()
    password = models.CharField(max_length=50,default='Hbet@123')

    class Meta:
        db_table = 'donor_details'
