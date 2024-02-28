from django.contrib import admin
from django.urls import path, include
from eventapp import views
urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/', include('allauth.urls')),

    path('', include('eventapp.urls')),
    path("accounts/", include("django.contrib.auth.urls")),
    path('update_webinar/<int:update_id>',views.update_webinar,name='update_webinar'),
    path('view_webinar/<int:update_id>',views.view_webinar,name='view_webinar'),
    path('register_for_webinar/<int:webinar_id>',views.register_for_webinar,name='register_for_webinar'),
    path('delete_webinar/<int:del_id>',views.delete_webinar,name='delete_webinar'),
    path('update_conference/<int:update_id>',views.update_conference,name='update_conference'),
    path('view_conference/<int:view_id>',views.view_conference,name='view_conference'),
    path('delete_conference/<int:del_id>',views.delete_conference,name='delete_conference'),
    path('payment/<int:pay_id>', views.payment, name='payment'),
    # path('service_payment/<int:book_id>', views.service_payment, name='service_payment'),
    path('service_paymenthandler/<int:book_id>', views.service_paymenthandler, name='service_paymenthandler'),
    path('viewservices/<int:service_id>',views.viewservices,name='viewservices'),
    path('availability/<int:service_id>',views.availability,name='availability'),
    path('book_services/<int:service_id>', views.book_services, name='book_services'),
    path('approve/<int:booking_id>/', views.approve_booking, name='approve_booking'),
    path('reject/<int:booking_id>/', views.reject_booking, name='reject_booking'),
    path('services_required/<int:webinar_id>', views.services_required, name='services_required'),
    path('pay_advance/<int:booking_id>/', views.pay_advance, name='pay_advance'),
    path('service_complete/<int:booking_id>/', views.service_complete, name='service_complete'),
]
