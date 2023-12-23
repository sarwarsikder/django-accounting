from django.contrib import admin
from .models import Document


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('doc_id', 'name', 'notes', 'date')
    search_fields = ('doc_id', 'notes')


admin.site.register(Document, DocumentAdmin)
