from datetime import datetime, date
from time import strptime
from urllib import request

import pymysql
from django.contrib import messages
import json
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from HBET.settings import ADMIN_CHECK
from HBETCODE import models
from HBETCODE.utilities.db import get_db_connection


# Create your views here.
def adminlogin(request):

    return render(request, "admin_login.html")

def admin_authentication(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if models.admin_details.objects.filter(email=username).exists() and models.admin_details.objects.filter(password=password).exists():
            return HttpResponseRedirect('/home')


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
        print(first_name, last_name, dob, dom, spouse_name, address1, address2, dor, city,state, pin_code, mobile2,mobile1, aadhar_card,pan_card,email)

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
    print(query)
    cur.execute(query)
    donor_data = cur.fetchall()
    #donor_data = json.dumps(donor_data,cls=DateEncoder)
    #context = {'donor_data': donor_data}
    print(type(donor_data))
    conn.commit()
    conn.close()
    return render(request, "edit_donor_details.html",{'rows': donor_data})
@csrf_exempt
def update_donor_details_db(request):

    if request.method == 'POST':
        data_q = request.POST.get('data')
        f_data = json.loads(data_q)

        for i in range(len(f_data)):
            print(i,"-----------------------------------")

            print(type(f_data[i]['Date Of Birth']),type(f_data[i]['Date Of Marriage']))
            print(f_data[i])
            id = int(f_data[i]['ID'])-1   #because we get start id in db from 1 and in list we get start id from 0
            print(id)
            first_name= f_data[i]['First name']
            last_name = f_data[i]['Last name']
            full_name = f_data[i]['Full Name']
            print(f_data[i]['Date Of Birth'], f_data[i]['Date Of Marriage'])
            dob = datetime.strptime(f_data[i]['Date Of Birth'], '%B %d, %Y').date()

            dom = 'NA' if f_data[i]['Date Of Marriage'] == '' or 'None' else datetime.strptime(f_data[i]['Date Of Marriage'], '%B %d, %Y').date()


            spouse_name = f_data[i]['Spouse Name']
            address1 = f_data[i]['Address 1']
            address2 = f_data[i]['Address 2']
            dor = datetime.strptime(f_data[i]['Date Of Registration'], '%B %d, %Y').date()
            city = f_data[i]['City']
            state = f_data[i]['State']
            pin_code = f_data[i]['Pincode']
            mobile1 = f_data[i]['Mobile Number 1']
            mobile2 = f_data[i]['Mobile Number 2']
            aadhar_card = f_data[i]['Aadhar Card Number']
            pan_card = f_data[i]['Pan Card Number']
            email = f_data[i]['Email']
            print(first_name, last_name, dob, dom, spouse_name, address1, address2, dor, city,
                  state, pin_code, mobile2,
                  mobile1, aadhar_card, pan_card,email,"in updateee")

            cur, conn = for_open_db_connection()

            query = f"update hbet.donor_details set first_name = '{first_name}', last_name = '{last_name}',full_name ='{full_name}', dob= '{dob}', dom = '{dom}', spouse_name = '{spouse_name}',address1 = '{address1}',address2 = '{address2}', dor ='{dor}',city = '{city}',state = '{state}', pin_code = '{pin_code}',mobile2 ='{mobile2}',mobile1 = '{mobile1}',aadhar_card = {aadhar_card}, pan_card='{pan_card}',email = '{email}' where id = {id+1}; "
            print(query)
            cur.execute(query)
            conn.commit()
            conn.close()



    return JsonResponse({'status': 'success'})


def for_open_db_connection():

        conn = get_db_connection()
        try:
            cur = conn.cursor(pymysql.cursors.DictCursor)

        except Exception as error:
            print(error)

        return cur,conn