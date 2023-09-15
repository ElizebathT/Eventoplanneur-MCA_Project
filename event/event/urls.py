from django.contrib import admin
from django.urls import path, include
from eventapp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('eventapp.urls')),
    path("accounts/", include("django.contrib.auth.urls")),
    path('update_webinar/<int:update_id>',views.update_webinar,name='update_webinar'),
    path('view_webinar/<int:update_id>',views.view_webinar,name='view_webinar'),
    path('delete_webinar/<int:del_id>',views.delete_webinar,name='delete_webinar'),
    path('update_conference/<int:update_id>',views.update_conference,name='update_conference'),
    path('view_conference/<int:view_id>',views.view_conference,name='view_conference'),
    path('delete_conference/<int:del_id>',views.delete_conference,name='delete_conference'),
]
