from django.contrib import admin

# Register your models here.


from django.contrib import admin
from .models import Measures, Inventory


class MeasuresAdmin(admin.ModelAdmin):
    list_display = ('measureID', 'measure')
    search_fields = ('measure',)


class InventoryAdmin(admin.ModelAdmin):
    list_display = (
    'inventoryID', 'inventory_item_name', 'account', 'inventory_type', 'measure', 'avg_price', 'avg_amount',
    'company_id', 'company_branch')
    search_fields = ('inventory_item_name', 'account__name', 'company_id__name', 'company_branch__name')
    list_filter = ('account', 'inventory_type', 'company_id', 'company_branch', 'measure')


admin.site.register(Measures, MeasuresAdmin)
admin.site.register(Inventory, InventoryAdmin)
