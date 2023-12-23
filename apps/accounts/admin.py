from django.contrib import admin
from .models import AccountLevel1, AccountLevel2, AccountLevel3


class AccountLevel1Admin(admin.ModelAdmin):
    list_display = ('level1ID', 'name')
    ordering = ('level1ID',)  # Use a negative sign to indicate descending order


class AccountLevel2Admin(admin.ModelAdmin):
    list_display = ('level2ID', 'name', 'level1ID')


class AccountLevel3Admin(admin.ModelAdmin):
    list_display = ('level3ID', 'name', 'level2ID')


admin.site.register(AccountLevel1, AccountLevel1Admin)
admin.site.register(AccountLevel2, AccountLevel2Admin)
admin.site.register(AccountLevel3, AccountLevel3Admin)
