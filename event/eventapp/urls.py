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
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)