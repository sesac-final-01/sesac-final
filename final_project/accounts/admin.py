from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['student_id']


admin.site.register(User, UserAdmin)
