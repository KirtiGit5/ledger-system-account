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
            'date': forms.DateInput(attrs={'type': 'date','placeholder': 'dd/mm/yyyy'}),
            'narration': forms.Textarea(attrs={'rows': 2}),
        }

# from django import forms
# from .models import ReceiptBookDeposit

# class ReceiptBookDepositForm(forms.ModelForm):
#     date = forms.DateField(
#         input_formats=['%d/%m/%Y'],  # Accept dd/mm/yyyy input
#         widget=forms.TextInput(
#             attrs={
#                 'class': 'form-control flatpickr',  # must match JS selector
#                 'placeholder': 'dd/mm/yyyy',
#                 'autocomplete': 'off'
#             }
#         )
#     )

#     class Meta:
#         model = ReceiptBookDeposit
#         fields = [
#             'member_name', 'member_mobile', 'date', 'month', 'year',
#             'debit_amount', 'credit_amount', 'narration'
#         ]
#         widgets = {
#             'narration': forms.Textarea(attrs={'rows': 2}),
#         }


