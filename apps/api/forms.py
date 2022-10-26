from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime

class GetTransactionsForm(forms.Form):
    account_id = forms.CharField(required=True, error_messages={'required': 'Account id not provided.'})
    date_from = forms.DateField(required=False, error_messages={'input_formats': 'Date format must be YYYY/MM/DD.'})
    date_to = forms.DateField(required=False, error_messages={'input_formats': 'Date format must be YYYY/MM/DD.'})
    country = forms.CharField(min_length = 2, max_length = 2, required=False, error_messages={'min_length': 'Country must use ISO-2 format.', 'max_length': 'Country must use ISO-2 format.'})

    def clean(self):
            cleaned_data = super(GetTransactionsForm, self).clean()
            
            date_from = self.cleaned_data['date_from']
            date_to = self.cleaned_data['date_to']
            today = datetime.date.today()

            if date_from and date_from > today:
                raise ValidationError('Date from cannot be in the future.', code='invalid')

            if date_to and date_to > today:
                raise ValidationError('Date to cannot be in the future.', code='invalid')

            if date_from and date_to:
                if date_from > date_to:
                    raise ValidationError('Date from cannot be larger than date to.', code='invalid')

            return cleaned_data

class GetAccountIdForm(forms.Form):
    account_id = forms.CharField(required=True, error_messages={'required': 'Account id not provided.'})

 