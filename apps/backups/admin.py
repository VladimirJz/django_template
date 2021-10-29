from django.contrib import admin

from apps.backups.models import Databases, ServerTypes, Servers,Databases,Jobs,Locations,Status

# Register your models here.
admin.site.register(Servers)
admin.site.register(ServerTypes)
admin.site.register(Databases)
admin.site.register(Jobs)
admin.site.register(Locations)
admin.site.register(Status)


