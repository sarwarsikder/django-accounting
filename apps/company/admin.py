from django.contrib import admin
from .models import Company, CompanyBranch


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'founded_date', 'website', 'email', 'phone_number', 'address')
    search_fields = ('name', 'email', 'phone_number')
    list_filter = ('founded_date',)
    date_hierarchy = 'founded_date'
    ordering = ('name',)


class CompanyBranchAdmin(admin.ModelAdmin):
    list_display = (
        'company', 'branch_name', 'branch_address', 'contact_person', 'contact_email', 'contact_phone_number')
    search_fields = ('company__name', 'branch_name', 'contact_person', 'contact_email', 'contact_phone_number')
    list_filter = ('company',)
    ordering = ('company', 'branch_name')


admin.site.register(CompanyBranch, CompanyBranchAdmin)
admin.site.register(Company, CompanyAdmin)
