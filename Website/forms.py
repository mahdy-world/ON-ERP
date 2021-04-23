from django import forms
from .models import *
from Invoices.models import *


class AddToCartForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['quantity']

