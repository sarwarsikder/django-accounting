from django.contrib import admin
from .models import DepreciationCategory, FixedAsset


class DepreciationCategoryAdmin(admin.ModelAdmin):
    list_display = ('accu_id', 'name', 'year', 'year_rate')
    search_fields = ('name', 'year')


class FixedAssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'brand', 'price', 'purchase_month', 'depreciation', 'identification', 'company_id',
                    'company_branch')
    search_fields = ('name', 'identification')
    list_filter = ('depreciation', 'purchase_month', 'company_id', 'company_branch')
    date_hierarchy = 'purchase_month'
    ordering = ('-purchase_month',)


admin.site.register(FixedAsset, FixedAssetAdmin)

admin.site.register(DepreciationCategory, DepreciationCategoryAdmin)
