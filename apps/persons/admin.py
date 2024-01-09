from django.contrib import admin
from .models import Person
from ..company.models import CompanyBranch


class PersonAdmin(admin.ModelAdmin):
    list_display = (
        'personsID', 'persons_name', 'user_name', 'company_id', 'company_branch', 'mobile', 'mobile2', 'occupation',
        'address', 'date_created', 'active', 'person_type')
    search_fields = ('persons_name', 'user_name', 'mobile', 'occupation', 'address')
    list_filter = ('company_id', 'company_branch', 'active', 'person_type')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'company_branch':
            company_id = request.GET.get('company_id') or getattr(request.resolver_match.kwargs, 'object_id', None)
            if company_id:
                kwargs['queryset'] = CompanyBranch.objects.filter(company_id=company_id)
            else:
                kwargs['queryset'] = CompanyBranch.objects.none()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Person, PersonAdmin)
