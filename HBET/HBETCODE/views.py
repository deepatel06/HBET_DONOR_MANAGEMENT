from datetime import datetime, date
from time import strptime
from urllib import request
from json import dumps
import pymysql
from django.contrib import messages
import json
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from HBET.HBETCODE import models
from HBET.HBETCODE.utilities.db import get_db_connection


# Create your views here.
def adminlogin(request):

    return render(request, "admin_login.html")

def admin_authentication(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if models.admin_details.objects.filter(email=username).exists() and models.admin_details.objects.filter(password=password).exists():
            return HttpResponseRedirect('/donorregistration')


        else:
            messages.error(request, 'Username or Password not correct')
            return HttpResponseRedirect('/')


def Home(request):
    return render(request, "home.html")

def donor_registration(request):

    return render(request, "donor_registration.html")

def insert_donor_details(request):
    if request.method == 'POST':
        first_name = request.POST['first-name']
        last_name = request.POST['last-name']
        full_name = first_name + ' ' + last_name
        dob = request.POST['dob']
        dom = request.POST['dom']
        spouse_name = request.POST['spouse-name']
        address1 = request.POST['address-1']
        address2 = request.POST['address-2']
        dor = request.POST['dor']
        city = request.POST['city']
        state = request.POST['state']
        pin_code = request.POST['pincode']
        mobile1 = request.POST['mobile-1']
        mobile2 = request.POST['mobile-2']
        aadhar_card = request.POST['aadhar']
        pan_card = request.POST['pan']
        email = request.POST['email']

        donor = models.DonorDetails(first_name=first_name, last_name=last_name, full_name =full_name, dob =dob, dom =dom,
                                    spouse_name =spouse_name,address1 =address1, address2=address2, dor=dor, city= city,
                                    state =state, pin_code=pin_code,mobile1= mobile1, mobile2= mobile2,
                                    aadhar_card= aadhar_card,pan_card=pan_card,email=email)
        donor.save()

        messages.success(request, 'Donor Registered successfully.')
        return HttpResponseRedirect('/donorregistration')

def donor_details(request):

    donor_data = models.DonorDetails.objects.all()
    return render(request, "donor_details.html", {'rows': donor_data})

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)
def edit_donor_details(request):

    #donor_data = models.DonorDetails.objects.all()
    #donor_data_forjs = list(donor_data.values())
    cur, conn = for_open_db_connection()

    query = f"SELECT * FROM hbet.donor_details;"
    cur.execute(query)
    donor_data = cur.fetchall()
    conn.commit()
    conn.close()
    dataJSON = dumps(donor_data,cls=DateEncoder)
    return render(request, "edit_donor_details.html",{'rows': donor_data,'dataJSON': dataJSON})
@csrf_exempt
def update_donor_details_db(request):

    if request.method == 'POST':
        data_q = request.POST.get('data')
        f_data = json.loads(data_q)

        for i in range(len(f_data)):
            id = int(f_data[i]['ID'])-1   #because we get start id in db from 1 and in list we get start id from 0
            first_name= f_data[i]['First name']
            last_name = f_data[i]['Last name']
            full_name = f_data[i]['Full Name']
            dob = datetime.strptime(f_data[i]['Date Of Birth'], '%B %d, %Y').date()
            dom = 'NA' if f_data[i]['Date Of Marriage'] == '' or 'None' else datetime.strptime(f_data[i]['Date Of Marriage'], '%B %d, %Y').date()
            spouse_name = f_data[i]['Spouse Name']
            address1 = f_data[i]['Address 1']
            address2 = f_data[i]['Address 2']
            dor = (f_data[i]['Date Of Registration'])
            city = f_data[i]['City']
            state = f_data[i]['State']
            pin_code = f_data[i]['Pincode']
            mobile1 = f_data[i]['Mobile Number 1']
            mobile2 = f_data[i]['Mobile Number 2']
            aadhar_card = f_data[i]['Aadhar Card Number']
            pan_card = f_data[i]['Pan Card Number']
            email = f_data[i]['Email']
            password = f_data[i]['Password']
            print(first_name, last_name,spouse_name, address1, address2,city,dob,dom,dor,
                  state, pin_code, mobile2,
                  mobile1, aadhar_card, pan_card,password,email,"in updateee")

            cur, conn = for_open_db_connection()
            query = f"update hbet.donor_details set first_name = '{first_name}', last_name = '{last_name}',full_name ='{full_name}', spouse_name = '{spouse_name}',address1 = '{address1}',address2 = '{address2}',city = '{city}',state = '{state}', pin_code = '{pin_code}',mobile2 ='{mobile2}',mobile1 = '{mobile1}',aadhar_card = {aadhar_card}, pan_card='{pan_card}',email = '{email}',dob ='{dob}',dom ='{dom}',dor ='{dor}'  where id = {id+1}; "
            print(query)
            cur.execute(query)
            conn.commit()
            conn.close()



    return JsonResponse({'status': 'success'})

def add_donation(request):

    return render(request, "add_donation.html")

def insert_donation(request):
    if request.method == 'POST':
        donation_type = request.POST['donation_type']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        contactno = request.POST['phone']
        typeofpayment = request.POST['payment_type']
        amount = request.POST['amount']
        dateofdonation = request.POST['dod']
        
        pan_no = request.POST['pan']
        email = request.POST['email']
        remarks  = request.POST['Remarks']
        print(donation_type, first_name, last_name, contactno, typeofpayment, amount, dateofdonation, pan_no, email,remarks)

        donation = models.Donation(first_name=first_name, last_name=last_name, type_of_donation=donation_type,
                                    type_of_payment =typeofpayment,amount =amount, date_of_donation=dateofdonation, contact_no=contactno,
                                    pan_no=pan_no, email=email,remarks=remarks)
        donation.save()

        messages.success(request, 'Donation added successfully.')
        return HttpResponseRedirect('/add_donation')

def viewDonation(request):
    donation_data = models.Donation.objects.all()
    return render(request, "view_donation.html", {'rows': donation_data})

def for_open_db_connection():

        conn = get_db_connection()
        try:
            cur = conn.cursor(pymysql.cursors.DictCursor)

        except Exception as error:
            print(error)

        return cur,conn 