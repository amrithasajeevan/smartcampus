from django.contrib import admin

from .models import *

from django.contrib.auth.admin import UserAdmin
# Register your models here.
# class CustomUserAdmin(UserAdmin):
#     model = CustomUser
#     # Customize how you want the admin panel to display your custom user model
#     list_display = ['username', 'email', 'first_name','middle_name', 'last_name', 'admission_number','date_of_birth', 'blood_group', 'place', 'phone_number', 'department', 'course', 'batch', 'start_year', 'end_year', 'barcode', 'image','is_staff']
#     # fieldsets = UserAdmin.fieldsets + (
#     #     (None, {'fields': ('admission_number', 'middle_name', 'date_of_birth', 'blood_group', 'place', 'phone_number', 'department', 'course', 'batch', 'start_year', 'end_year', 'barcode', 'image')}),
#     # )

admin.site.register(CustomUser)