# forms.py

from django import forms

from apps.persons.models import Person


class PersonFormCreate(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['persons_name', 'user_name', 'mobile', 'mobile2', 'occupation', 'address', 'active', 'person_type']
        widgets = {
            'persons_name': forms.TextInput(attrs={'class': 'form-control'}),
            'user_name': forms.TextInput(attrs={'class': 'form-control'}),
            # 'company_id': forms.Select(attrs={'class': 'form-select'}),
            # 'company_branch': forms.Select(attrs={'class': 'form-select'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile2': forms.TextInput(attrs={'class': 'form-control'}),
            'occupation': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'active': forms.Select(attrs={'class': 'form-select'}),
            'person_type': forms.Select(attrs={'class': 'form-select'}),
        }


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['persons_name', 'user_name', 'mobile', 'mobile2', 'occupation', 'address', 'active', 'person_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add Bootstrap classes to form fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        # Optionally, you can add additional Bootstrap classes to specific fields
        # self.fields['persons_name'].widget.attrs['class'] += ' custom-class'
        # self.fields['company_id'].widget.attrs['class'] += ' custom-class'
        # Add more fields as needed
