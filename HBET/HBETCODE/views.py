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
from django.contrib.auth import logout
from django.shortcuts import redirect
import pandas as pd

from HBETCODE import models
from HBETCODE.utilities.db import get_db_connection


# Create your views here.

def my_login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
       
        if "user_email" in request.session :
            
            return view_func(request, *args, **kwargs)
        else:
            
            return HttpResponseRedirect('/')  # Redirect to login page if not authenticated
    return _wrapped_view

def adminlogin(request):
    return render(request, "admin_login.html")

def admin_authentication(request):
    if request.method == 'POST':
        useremail = request.POST['username']
        password = request.POST['password']
        
        if models.admin_details.objects.filter(email=useremail).exists() and models.admin_details.objects.filter(password=password).exists():
            request.session['user_email'] = useremail
            admin_data = models.admin_details.objects.filter(email=useremail).values()
            for user in admin_data:
                request.session['user_name'] = user['full_name']
                print(user['full_name'])
            return HttpResponseRedirect('/donorregistration')


        else:
            messages.error(request, 'Username or Password not correct')
            return HttpResponseRedirect('/')


def Home(request):
    return render(request, "home.html")

@my_login_required
def donor_registration(request):
    session_username = request.session['user_name']
    
    return render(request, "donor_registration.html",{'username': session_username})

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
@my_login_required
def donor_details(request):
    session_username = request.session['user_name']
    donor_data = models.DonorDetails.objects.all()
    return render(request, "donor_details.html", {'rows': donor_data, 'username': session_username}) 

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)
@my_login_required    
def edit_donor_details(request):

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
            first_name= f_data[i]['First Name']
            last_name = f_data[i]['Last Name']
            full_name = f_data[i]['Full Name']
            dob = f_data[i]['Date Of Birth(YYYY-MM-DD)']
            dom = f_data[i]['Date Of Marriage']
            spouse_name = f_data[i]['Spouse Name']
            address1 = f_data[i]['Address 1']
            address2 = f_data[i]['Address 2']
            dor = f_data[i]['Date Of Registration']
            city = f_data[i]['City']
            state = f_data[i]['State']
            pin_code = f_data[i]['Pincode']
            mobile1 = f_data[i]['Mobile Number 1']
            mobile2 = f_data[i]['Mobile Number 2']
            aadhar_card = f_data[i]['Aadhar Card Number']
            pan_card = f_data[i]['Pan Card Number']
            email = f_data[i]['Email']
            password = f_data[i]['Password']
            
            cur, conn = for_open_db_connection()
            query = f"update hbet.donor_details set first_name = '{first_name}', last_name = '{last_name}',full_name ='{full_name}', spouse_name = '{spouse_name}',address1 = '{address1}',address2 = '{address2}',city = '{city}',state = '{state}', pin_code = '{pin_code}',mobile2 ='{mobile2}',mobile1 = '{mobile1}',aadhar_card = {aadhar_card}, pan_card='{pan_card}',email = '{email}',dob ='{dob}',dom ='{dom}',dor ='{dor}'  where id = {id+1}; "
            
            cur.execute(query)
            conn.commit()
            conn.close()



    return JsonResponse({'status': 'success'})

@my_login_required
def add_donation(request):
    session_username = request.session['user_name']
    sql = f"""select distinct full_name,mobile1 from donor_details;"""
    cur, conn = for_open_db_connection()
    df_cu = pd.read_sql(sql, conn)
    
    donor_name_dict = {}
    for _, row in df_cu.iterrows():
        donor_name_dict[row["full_name"]] = {}
        donor_name_dict[row["full_name"]]["contact_no"] = row["mobile1"]
        donor_name_dict[row["full_name"]]["name"] = row["full_name"]
    
    dataJSON = dumps(donor_name_dict)
  
    return render(request, "add_donation.html",{'username': session_username,'donor_dict':dataJSON})

def insert_donation(request):
    if request.method == 'POST':
        donation_type = request.POST['donation_type']
        full_name = request.POST['firstname']
        
        contactno = request.POST['phone']
        typeofpayment = request.POST['payment_type']
        amount = request.POST['amount']
        dateofdonation = request.POST['dod']
        
        remarks  = request.POST['Remarks']
      
        cur, conn = for_open_db_connection()
        query = f"SELECT first_name,last_name,email,pan_card FROM hbet.donor_details where full_name = '{full_name}' and mobile1= {contactno};"
        
        cur.execute(query)
        donor_data = cur.fetchall()
        conn.commit()
        conn.close()
        
        first_name = donor_data[0]["first_name"]
        last_name = donor_data[0]["last_name"]
        email = donor_data[0]["email"]
        pan_no = donor_data[0]["pan_card"]
        

        print(donation_type, first_name, last_name, contactno, typeofpayment, amount, dateofdonation, pan_no, email,remarks)

        donation = models.Donation(first_name=first_name, last_name=last_name, type_of_donation=donation_type,
                                    type_of_payment =typeofpayment,amount =amount, date_of_donation=dateofdonation, contact_no=contactno,
                                    pan_no=pan_no, email=email,remarks=remarks)
        donation.save()

        messages.success(request, 'Donation added successfully.')
        return HttpResponseRedirect('/add_donation')
@my_login_required
def viewDonation(request):
    donation_data = models.Donation.objects.all()
    session_username = request.session['user_name']
    return render(request, "view_donation.html", {'rows': donation_data,'username': session_username})

def for_open_db_connection():

        conn = get_db_connection()
        try:
            cur = conn.cursor(pymysql.cursors.DictCursor)

        except Exception as error:
            print(error)

        return cur,conn 
def logout_view(request):
    # Clear the user's session data
    del request.session['user_email']
        # Log the user out using Django's built-in logout function
    
    
    # Redirect the user to a specific page (optional)
    return HttpResponseRedirect('/')
    
