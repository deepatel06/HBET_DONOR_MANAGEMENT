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
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Donation  # import your Donation model



from django.template.loader import get_template
from reportlab.pdfgen import canvas
from io import BytesIO

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib
import os


from django.contrib.auth import update_session_auth_hash


from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch


from HBETCODE import models
from HBETCODE.utilities.db import get_db_connection


def my_login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
       
        if "user_email" in request.session :
            
            return view_func(request, *args, **kwargs)
        else:
            
            return HttpResponseRedirect('/')  # Redirect to login page if not authenticated
    return _wrapped_view

@my_login_required
def download_excel(request):
    cur, conn = for_open_db_connection()

    query= f"SELECT * FROM hbet.donor_details;"

    cur.execute(query)
    donation_details = cur.fetchall()

    conn.commit()
    conn.close()

    donor_details_array = []

    for row in donation_details:
        row['aadhar_card'] = str(row['aadhar_card'])
        donor_details_array.append(row)

    # Create a DataFrame from the data
    df = pd.DataFrame(donor_details_array)

    # Create a response object
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=donor_details.xlsx'

    # Save the DataFrame to the response as an Excel file
    df.to_excel(response, index=False, sheet_name='Donor Details')

    return response

@my_login_required
def donor_details(request):
    username = request.session['user_name']
    cur, conn = for_open_db_connection()

    query= f"SELECT * FROM hbet.donor_details;"

    cur.execute(query)
    donation_details = cur.fetchall()

    conn.commit()
    conn.close()

    donor_details_array = []

    for row in donation_details:
        row['dor'] = row['dor'].strftime('%Y-%m-%d')
        row['dob'] = row['dob'].strftime('%Y-%m-%d')
        donor_details_array.append(row)

    return render(request, 'donor_details.html', {'donor_details_array': donor_details_array, 'username': username})


def update_doner_details_page(request):
    cur, conn = for_open_db_connection()

    query= f"SELECT * FROM hbet.donor_details;"

    cur.execute(query)
    donation_details = cur.fetchall()

    conn.commit()
    conn.close()

    donor_details_array = []

    for row in donation_details:
        row['dor'] = row['dor'].strftime('%Y-%m-%d')
        row['dob'] = row['dob'].strftime('%Y-%m-%d')
        donor_details_array.append(row)

    return render(request, 'update_donor_details.html', {'donor_details_array': donor_details_array})

def update_donor_details(request, id):
    if request.method == 'POST':

        first_name = request.POST['fname']
        lname = request.POST['lname']
        fullname = request.POST['fullname']
        spname = request.POST['spname']
        add1 = request.POST['add1']
        add2 = request.POST['add2']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']
        mob1 = request.POST['mob1']
        mob2 = request.POST['mob2']
        aacard = request.POST['aacard']
        pacard = request.POST['pacard']
        email = request.POST['email']
        dob = request.POST['dob']
        dom = request.POST['dom']
        dor = request.POST['dor']

        cur, conn = for_open_db_connection()
        

        query= f"update hbet.donor_details set first_name = '{first_name}', last_name = '{lname}',full_name ='{fullname}', spouse_name = '{spname}',address1 = '{add1}',address2 = '{add2}',city = '{city}',state = '{state}', pin_code = '{pincode}',mobile2 ='{mob2}',mobile1 = '{mob1}',aadhar_card = {aacard}, pan_card='{pacard}',email = '{email}',dob ='{dob}',dom ='{dom}',dor ='{dor}'  where id = '{id}'; "
        cur.execute(query)
        conn.commit()
        conn.close()

        return HttpResponseRedirect('/view_donor_details')

def donation_type_operations(request):
    active_user = request.session['user_name']
    
    cur, conn = for_open_db_connection()

    query= f"SELECT donation_type FROM hbet.donation_type;"

    cur.execute(query)
    donation_types = cur.fetchall()

    conn.commit()
    conn.close()

    donation_type_array=[]

    for row in donation_types:
        array_value = row["donation_type"]
        donation_type_array.append(array_value)

    return render(request, 'donation_add_del.html', {'username': active_user, 'donation_type_array': donation_type_array })


def delete_donation_type(request, donation_type):

    cur, conn = for_open_db_connection()
    
    query= f"DELETE FROM `hbet`.`donation_type` WHERE (`donation_type` = '{donation_type}');"
    cur.execute(query)
    conn.commit()
    conn.close()

    return HttpResponseRedirect('/donation_type_operations')


def add_donation_type(request):
    username = request.session['user_name']
    if request.method == 'POST':
        n_don_type = request.POST['n_don_type']

        cur, conn = for_open_db_connection()

        query2= f"INSERT INTO donation_type (donation_type) VALUES ('{n_don_type}');"
        cur.execute(query2)
        conn.commit()
        conn.close()

        return HttpResponseRedirect('/donation_type_operations')

    else:
        return HttpResponseRedirect(request.path_info, {'username': username })

def adminlogin(request):
    return render(request, "admin_login.html")

def forget_password(request):
    if request.method=='POST':
        fpemail1 = request.POST['fpemail'] 
        cur, conn = for_open_db_connection()

        query= f"SELECT * FROM hbetcode_admin_details WHERE email = '{fpemail1}'; "
        cur.execute(query)
        
        fp_req = cur.fetchall()

        if not fp_req:
            messages.info(request, "Email Does Not Exists")
            return render(request, "admin_login.html")
        
        print(fp_req)
        conn.commit()
        conn.close()

        use_email=fp_req[0]['email']
        use_pass=fp_req[0]['password']

        print(use_email, use_pass)

        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.ehlo()
        smtp.starttls()

        smtp.login('deep@aivantage.org', 'mmxmbdyyeazffslr')
        
        subject = 'Login Credentials'
        context = {
            'Email': use_email,
            'Password': use_pass,
        }
        template = render_to_string("forget_password.html", context)

        msg = message(subject, html=template)
        to = use_email

        smtp.sendmail(from_addr="deep@aivantage.org", to_addrs=to, msg=msg.as_string())
        smtp.quit()

        messages.info(request, "Mail Sent succesfully")

    return render(request, "admin_login.html")


@my_login_required
def reset_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        user=request.session['user_email']
        username = request.session['user_name']
        cur, conn = for_open_db_connection()

        query1= f"SELECT password FROM hbetcode_admin_details WHERE email = '{user}'; "
        cur.execute(query1)
        
        rp_req = cur.fetchall()

        use_pass=rp_req[0]['password']

        if old_password != use_pass:
            return messages.info(request, "Incorrect Current Password")

        if new_password1 != new_password2:
            return  messages.info(request, "New Password and Confirm New Password Does Not Match")

        query2 = f"UPDATE hbetcode_admin_details SET password = '{new_password2}' WHERE email = '{user}'; "
        cur.execute(query2)

        messages.info(request,"Password updated succesfully")

        conn.commit()
        conn.close()

        return render(request, 'donor_registration.html',{'username': username })
    
    else:
        return render(request, 'reset_password.html')
        

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
 

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)

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

    query1= f"SELECT donation_type FROM hbet.donation_type;"
    cur.execute(query1)
    do_t = cur.fetchall()

    donation_array=[]

    for row in do_t:
        array_value = row["donation_type"]
        donation_array.append(array_value)


    return render(request, "add_donation.html",{'username': session_username,'donor_dict':dataJSON, 'donation_array': donation_array })

def insert_donation(request):
    if request.method == 'POST':
        donation_type = request.POST['donation_type']
        full_name = request.POST['firstname']
        
        contactno = request.POST['phone']
        typeofpayment = request.POST['payment_type']
        amount = request.POST['amount']
        dateofdonation = request.POST['dod']


        cheque_no = request.POST['cheque_number']
        bank_name = request.POST['bank_name']
        transaction_id = request.POST['transaction_id']
        
        
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
                                    pan_no=pan_no, email=email,remarks=remarks,cheque_no=cheque_no,bank_name=bank_name,transaction_id=transaction_id)
        donation.save()

        donation_submission(full_name,amount,dateofdonation,typeofpayment,donation_type,email)

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

def donation_submission(firstname, amount, dod, payment_type, donation_type, email):
    # Send the receipt email
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()

    # Login with your email and password
    smtp.login('deep@aivantage.org', 'mmxmbdyyeazffslr')
    
    subject = 'Donation Receipt'
    context = {
        'full_name': firstname,
        'amount': amount,
        'date': dod,
        'payment_type': payment_type,
        'type_of_donation': donation_type,
    }
    template = render_to_string("invoice.html", context)
    pdf_attachment = generate_pdf('invoice.html', context)

    msg = message(subject, html=template)
    to = ["deeppatel61098.d@gmail.com", "meetdave1902@gmail.com"]

    # Attach the PDF to the email
    pdf_part = MIMEApplication(pdf_attachment.content)
    pdf_part.add_header('Content-Disposition', 'attachment', filename="receipt.pdf")
    msg.attach(pdf_part)

    # Send the email using the smtp server
    smtp.sendmail(from_addr="deep@aivantage.org", to_addrs=to, msg=msg.as_string())
    smtp.quit()

def generate_pdf(template, context):
    template = get_template(template)
    html = template.render(context)  # Provide context to render the template

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="output.pdf"'
     # Generate the PDF using the ReportLab canvas

    p = canvas.Canvas(response, pagesize=landscape(letter))

    # Set font and font size for the header
    p.setFont("Helvetica-Bold", 18)

    # Decorate organization name with color and font style
    org_name = "Harbans Bhalla Education Trust"
    p.setFillColor(colors.darkblue)
    org_name_width = p.stringWidth(org_name, "Helvetica-Bold", 18)
    org_name_x = (p._pagesize[0] - org_name_width) / 2
    p.drawCentredString(org_name_x, 520, org_name)

    # Set font for the rest of the content
    p.setFont("Helvetica", 12)

    # Draw title with improved formatting
    p.drawString(40, 480, "Donation Receipt")

    # Draw line under the title
    p.line(40, 475, 556, 475)

    # Draw donor details with enhanced alignment
    details = [
        ("Recipient:", context['full_name']),
        ("Date:", context['date']),
        ("Type of Donation:", context['type_of_donation']),
        ("Amount:", context['amount']),
        
    ]

    y_position = 440
    for label, value in details:
        p.setFillColor(colors.black)
        p.drawString(40, y_position, label)
        p.drawString(200, y_position, value)
        y_position -= 20

    # Draw a line separator
    p.line(40, 330, 556, 330)

    # Draw Trust address with improved styling
    trust_address = [
        "Harbans Bhalla Education Trust",
        "123 Main Street, Cityville, Country",
        "Phone: (123) 456-7890",
        "Email: info@hbet.org",
        "PAN No: ABCDE1234F"
    ]

    y_position = 200
    for line in trust_address:
        p.setFillColor(colors.black)
        p.drawString(40, y_position, line)
        y_position -= 14

    # Decorate thank you message with a different font and color
    p.setFont("Helvetica-Oblique", 16)
    thank_you_message = "Thank you for your generous donation!"
    thank_you_width = p.stringWidth(thank_you_message, "Helvetica-Oblique", 16)
    thank_you_x = (p._pagesize[0] - thank_you_width) / 2
    p.setFillColor(colors.green)
    p.drawCentredString(thank_you_x, 100, thank_you_message)

    # Save the page
    p.showPage()
    p.save()
    return response
 
def logout_view(request):
    # Clear the user's session data
    del request.session['user_email']
        # Log the user out using Django's built-in logout function
    
    # Redirect the user to a specific page (optional)
    return HttpResponseRedirect('/')

# send our email message 'msg' to our boss
def message(subject="Thank You!",
            html="", img=None,
            attachment=None):
    # build message contents
    msg = MIMEMultipart()
    
    # Add Subject
    msg['Subject'] = subject
    
    # Add text contents
    # Create the MIME message
    message = MIMEMultipart("alternative")
    msg.attach(MIMEText(html,'html'))
 

    # Check if we have anything
    # given in the img parameter
    if img is not None:
        
        # Check whether we have the lists of images or not!
        if type(img) is not list:
            
            # if it isn't a list, make it one
            img = [img]

        # Now iterate through our list
        for one_img in img:
            
            # read the image binary data
            img_data = open(one_img, 'rb').read()
            # Attach the image data to MIMEMultipart
            # using MIMEImage, we add the given filename use os.basename
            msg.attach(MIMEImage(img_data,
                                name=os.path.basename(one_img)))

    # We do the same for
    # attachments as we did for images
    if attachment is not None:
        
        # Check whether we have the
        # lists of attachments or not!
        if type(attachment) is not list:
            
            # if it isn't a list, make it one
            attachment = [attachment]

        for one_attachment in attachment:

            with open(one_attachment, 'rb') as f:
                
                # Read in the attachment
                # using MIMEApplication
                file = MIMEApplication(
                    f.read(),
                    name=os.path.basename(one_attachment)
                )
            file['Content-Disposition'] = f'attachment;\
            filename="{os.path.basename(one_attachment)}"'
            
            # At last, Add the attachment to our message object
            msg.attach(file)
    return msg
