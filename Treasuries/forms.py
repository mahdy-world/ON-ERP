from django import forms
from .models import *


class TreasuryForm(forms.ModelForm):
    class Meta:
        model = Treasury
        exclude = ['deleted']

class TreasuryDeleteForm(forms.ModelForm):
    class Meta:
        model = Treasury
        fields = ['deleted']

class PaymentMachinesForm(forms.ModelForm):
    class Meta:
        model = PaymentMachines
        exclude = ['deleted']
        fields = ['name', 'discount_percentage', 'transfer']
    
class PaymentMachinesDeleteForm(forms.ModelForm):
    class Meta:
        model = PaymentMachines
        fields = ['deleted']    




