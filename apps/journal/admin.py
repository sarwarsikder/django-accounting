from django.contrib import admin

from .models import Document, Transaction


class TransactionInline(admin.StackedInline):
    model = Transaction
    extra = 1
    exclude = ('notes', 'created_at', 'updated_at', 'date', 'created_by', 'updated_by')


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('doc_id', 'date', 'name', 'created_by', 'updated_by')
    search_fields = ('name',)
    inlines = [TransactionInline]
    exclude = ('created_by', 'updated_by')


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'doc_id', 'account', 'customer', 'date', 'debit', 'credit')
    search_fields = ('doc_id__name', 'account__name', 'customer__persons_name')
    list_filter = ('account', 'customer')


admin.site.register(Document, DocumentAdmin)
admin.site.register(Transaction, TransactionAdmin)
