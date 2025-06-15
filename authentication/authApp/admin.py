from django.contrib import admin
from .models import Account
# Register your models here.
class AccountAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'is_active']
    list_display_links = ['first_name', 'last_name', 'email']
    list_editable = ['is_active']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['p_name', 'id']

admin.site.register(Account,AccountAdmin)
