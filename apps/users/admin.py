from django.contrib import admin

from .models import CustomUser, Company, CompanyBranch


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'company', 'company_branch', 'mobile', 'address', 'is_staff')
    search_fields = ('username', 'email', 'company__name', 'company_branch__name', 'mobile', 'address')
    ordering = ('username',)


class CompanyInline(admin.TabularInline):
    model = Company
    extra = 1


class CompanyBranchInline(admin.TabularInline):
    model = CompanyBranch
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'company':
            kwargs['queryset'] = Company.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(CustomUser, CustomUserAdmin)
