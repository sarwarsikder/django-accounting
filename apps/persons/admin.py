from django.contrib import admin

from apps.persons.models import Person


class PersonAdmin(admin.ModelAdmin):
    list_display = (
        'personsID', 'persons_name', 'company_id', 'company_branch', 'mobile', 'address', 'date_created', 'active',
        'person_type')
    list_filter = ('company_id', 'company_branch', 'active', 'person_type')
    search_fields = ('persons_name', 'mobile', 'address')


admin.site.register(Person, PersonAdmin)
