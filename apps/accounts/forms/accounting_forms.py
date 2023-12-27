# forms.py

from django import forms
from ..models import AccountLevel1, AccountLevel2, AccountLevel3, Account


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['level1', 'level2', 'level3', 'name', 'account_code']

    level1 = forms.ModelChoiceField(
        queryset=AccountLevel1.objects.all(),
        required=True,
        label='Account Level 1',
        widget=forms.Select(attrs={'class': 'form-select level1-dropdown'}),
    )

    level2 = forms.ModelChoiceField(
        queryset=AccountLevel2.objects.none(),
        required=True,
        label='Account Level 2',
        widget=forms.Select(attrs={'class': 'form-select level2-dropdown'}),
    )

    level3 = forms.ModelChoiceField(
        queryset=AccountLevel3.objects.none(),
        required=True,
        label='Account Level 3',
        widget=forms.Select(attrs={'class': 'form-select level3-dropdown'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add Bootstrap classes to each field
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'  # You can customize this class based on Bootstrap styles

        # Dynamically set choices for level2 and level3 based on the selected level1
        if 'level1' in self.data:
            try:
                level1_id = int(self.data.get('level1'))
                self.fields['level2'].queryset = AccountLevel2.objects.filter(level1ID=level1_id)
            except (ValueError, TypeError):
                pass  # Invalid input from the client; ignore and fallback to default choices

        if 'level2' in self.data:
            try:
                level2_id = int(self.data.get('level2'))
                self.fields['level3'].queryset = AccountLevel3.objects.filter(level2ID=level2_id)
            except (ValueError, TypeError):
                pass  # Invalid input from the client; ignore and fallback to default choices


class AccountFormEdit(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['level1ID', 'level2ID', 'level3ID', 'name', 'account_code']

    def __init__(self, *args, **kwargs):
        super(AccountFormEdit, self).__init__(*args, **kwargs)

        # Add Bootstrap classes to each field
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'  # You can customize this class based on Bootstrap styles

        # Preselect the dropdown values if the instance exists
        # if self.instance:
        #     self.fields['level3ID'].queryset = AccountLevel3.objects.filter(level2ID=self.instance.level2ID)
        #     self.fields['level2ID'].queryset = AccountLevel2.objects.filter(level1ID=self.instance.level1ID)
        #     self.fields['level1ID'].queryset = AccountLevel1.objects.all()
        #
        #     # Set initial values with instances
        #     self.initial['level3ID'] = self.instance.level3ID
        #     self.initial['level2ID'] = self.instance.level2ID
        #     self.initial['level1ID'] = self.instance.level1ID

    def clean(self):
        cleaned_data = super(AccountFormEdit, self).clean()

        # Access the correct keys in cleaned_data
        level1_instance = cleaned_data.get('level1ID')
        level2_instance = cleaned_data.get('level2ID')
        level3_instance = cleaned_data.get('level3ID')

        # Additional validation if needed

        return cleaned_data
