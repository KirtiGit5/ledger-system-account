from django import forms
from .models import ReceiptBookDeposit

class ReceiptBookDepositForm(forms.ModelForm):
    class Meta:
        model = ReceiptBookDeposit
        fields = [
            'member_name', 'member_mobile', 'date', 'month', 'year',
            'debit_amount', 'credit_amount', 'narration'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'narration': forms.Textarea(attrs={'rows': 2}),
        }