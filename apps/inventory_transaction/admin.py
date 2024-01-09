from django.contrib import admin
from .models import InventoryTransaction


class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = ('inv_transID', 'doc_id', 'inventory', 'supplier', 'company_id', 'company_branch',
                    'unit', 'price', 'total_price', 'discount', 'expense_type', 'vehicle',
                    'note', 'status', 'date', 'created_by', 'updated_by', 'created_at', 'updated_at')
    search_fields = ('inventory__name', 'supplier__persons_name', 'expense_type__name', 'vehicle__name')
    list_filter = ('status', 'date', 'created_at', 'updated_at')
    exclude = ('created_by', 'updated_by')


admin.site.register(InventoryTransaction, InventoryTransactionAdmin)
