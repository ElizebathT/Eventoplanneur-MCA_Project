from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from django.contrib.auth import views as auth_views

app_name = 'eventapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('orghome/', views.orghome, name='orghome'),
    path('attendeehome/', views.attendeehome, name='attendeehome'),
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('logout/',views.logout,name='logout'),
    path('webinar/',views.webinar,name='webinar'),
    path('register_webinar/',views.register_webinar,name='register_webinar'),
    path('reset_password/',auth_views.PasswordResetView.as_view(),name="reset_password"),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"), 
    path('reg_organizer/',views.reg_organizer,name='reg_organizer'),
    path('reg_provider/',views.reg_provider,name='reg_provider'),
    path('reg_attendee/',views.reg_attendee,name='reg_attendee'),
    path('org_profile/',views.org_profile,name='org_profile'),
    path('attendee_profile/',views.attendee_profile,name='attendee_profile'),
    path('check_aicte_id/', views.check_aicte_id, name='check_aicte_id'),
    path('conference/',views.conference,name='conference'),
    path('register_conference/',views.register_conference,name='register_conference'),
    path('listwebinars/',views.listwebinars,name='listwebinars'),
    path('events/',views.events,name='events'),
    path('verify/',views.verify,name='verify'),
    path('registered_webinar/',views.registered_webinar,name='registered_webinar'),
    path('gallery/',views.gallery,name='gallery'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('paymentsuccess/', views.paymentsuccess, name='paymentsuccess'),
    path('paymentfail/', views.paymentfail, name='paymentfail'),
    path('admindash/', views.admindash, name='admindash'),
    path('recommendations/', recommendations, name='recommendations'),
    path('providerhome/', views.providerhome, name='providerhome'),
    path('services/', views.services, name='services'),
    path('addservices/', views.addservices, name='addservices'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)