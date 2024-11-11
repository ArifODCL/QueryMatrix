from django.contrib import admin
from account.models import *
# Register your models here.


@admin.register(DesignationModel)
class DesignationModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'phone']
    search_fields = ['first_name', 'last_name', 'email', 'phone']


@admin.register(EmployeeModel)
class EmployeeModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'designation', 'date_of_join']
    search_fields = ['user', 'designation', 'date_of_join']