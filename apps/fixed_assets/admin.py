from django.contrib import admin
from .models import DepreciationCategory


class DepreciationCategoryAdmin(admin.ModelAdmin):
    list_display = ('accu_id', 'name', 'year', 'year_rate')
    search_fields = ('name', 'year')


admin.site.register(DepreciationCategory, DepreciationCategoryAdmin)
