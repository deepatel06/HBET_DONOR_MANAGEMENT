from django.urls import path
from . import views

urlpatterns = {
    path('', views.adminlogin, name='admin login'),
    path('home', views.Home, name='home'),
    #path('donordetails', views.donor_details, name='donor details'),
    #path('editdonordetails', views.edit_donor_details, name='edit donor details'),
    #path('updatedonordetailsdb', views.update_donor_details_db, name='update donor details in db'),
    path('donorregistration', views.donor_registration, name='donor registration'),
    path('insertdonor', views.insert_donor_details, name='insert donor'),
    path('admin_authentication', views.admin_authentication, name='admin_authentication'),
    path('add_donation', views.add_donation, name='add_donation'),
    path('insert_donation', views.insert_donation, name='insert_donation'),
    path('view_donation', views.viewDonation, name='view_donation'),
    path('logout', views.logout_view, name='logout'),
    path('forget_password', views.forget_password, name='forget_password'),
    path('reset_password', views.reset_password, name='reset_password'),
    path('add_donation_type', views.add_donation_type, name='add_donation_type'),
    path('donation_type_operations', views.donation_type_operations, name='donation_operations'),
    path('delete_donation_type/<donation_type>', views.delete_donation_type, name='delete_donation'),
    ## I need to remove 
    path('view_donor_details', views.donor_details, name='see_donor_details'),
    path('update_donor_details_page', views.update_doner_details_page, name='update_details_page'),
    path('update_doner_details/<id>', views.update_donor_details, name='update_donor_detail'),
    path('download_donor_details', views.download_excel, name='download_excel'),
}
