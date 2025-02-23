from django.contrib import admin

from apps.models import Application, ApplicationType, Admin


@admin.register(ApplicationType)
class ApplicationTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    pass


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    pass
