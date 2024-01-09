from django.contrib import admin
from .models import AccountLevel1, AccountLevel2, AccountLevel3
from .models import Account
from django import forms


class AccountAdminForm(forms.ModelForm):
    account_code = forms.CharField(label='Account Code', max_length=3, required=False)

    class Meta:
        model = Account
        fields = '__all__'
        exclude = ('accountID',)


class AccountLevel1Admin(admin.ModelAdmin):
    list_display = ('level1ID', 'name')
    ordering = ('level1ID',)  # Use a negative sign to indicate descending order


class AccountLevel2Admin(admin.ModelAdmin):
    list_display = ('level2ID', 'name', 'level1ID')


class AccountLevel3Admin(admin.ModelAdmin):
    list_display = ('level3ID', 'name', 'level2ID')


class AccountAdmin(admin.ModelAdmin):
    form = AccountAdminForm
    list_display = (
        'accountID', 'level1ID', 'level2ID', 'level3ID', 'name', 'company_id', 'company_branch', 'created_by',
        'updated_by', 'created_at',
        'updated_at')
    search_fields = ('name',)
    list_filter = ('company_id', 'company_branch', 'created_at', 'updated_at')

    def save_model(self, request, obj, form, change):
        # Set level3ID based on company_id
        obj.accountID = str(obj.level3ID) + str(obj.account_code)
        super().save_model(request, obj, form, change)


admin.site.register(Account, AccountAdmin)
admin.site.register(AccountLevel1, AccountLevel1Admin)
admin.site.register(AccountLevel2, AccountLevel2Admin)
admin.site.register(AccountLevel3, AccountLevel3Admin)
