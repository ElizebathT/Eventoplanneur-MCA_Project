from django.contrib import admin
from .models import CustomUser,Webinar,EventOrganizer,AICTE,Speaker,Program,Department

admin.site.register(CustomUser)
admin.site.register(Webinar)
admin.site.register(EventOrganizer)
admin.site.register(AICTE)
admin.site.register(Program)
admin.site.register(Department)
admin.site.register(Speaker)