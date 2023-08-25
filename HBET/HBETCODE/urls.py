from django.urls import path
from . import views

urlpatterns = {
    path('', views.adminlogin, name='admin login'),
    path('home', views.Home, name='home'),
    path('donordetails', views.donor_details, name='donor details'),
    path('editdonordetails', views.edit_donor_details, name='edit donor details'),
    path('updatedonordetailsdb', views.update_donor_details_db, name='update donor details in db'),
    path('donorregistration', views.donor_registration, name='donor registration'),
    path('insertdonor', views.insert_donor_details, name='insert donor'),
    path('admin_authentication', views.admin_authentication, name='admin_authentication'),
    path('add_donation', views.add_donation, name='add_donation'),
    path('insert_donation', views.insert_donation, name='insert_donation'),
    path('view_donation', views.viewDonation, name='view_donation'),
    path('logout', views.logout_view, name='logout'),
    path('forget_password', views.forget_password, name='forget_password'),
    path('reset_password', views.reset_password, name='reset_password')
}
