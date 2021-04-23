from django import forms

from .models import *
#
#

class SalesInvoiceForm(forms.ModelForm):
    class Meta:
        model = MagedInvoice
        fields = [
            'after_discount',
            'internal_comment',
        ]
        widgets = {
            'after_discount': forms.NumberInput(attrs={'readonly': 'readonly'}),
        }

class SalesPaidInvoiceForm(forms.ModelForm):
    class Meta:
        model = MagedInvoice
        exclude = ['customer_credit']
        fields = [
            'after_discount',
            'incoming',
            'comment',
        ]
        labels = {
            'incoming': 'مدفوع',
        }
        widgets = {
            'after_discount': forms.NumberInput(attrs={'readonly': 'readonly'}),
        }

class OutInvoiceForm(forms.ModelForm):
    class Meta:
        model = MagedInvoice
        fields = [
            'numbering',
        ]
#

class PurchaseInvoiceForm(forms.ModelForm):
    class Meta:
        model = MagedInvoice
        fields = [
            'after_discount',
            'internal_comment',
        ]
        widgets = {
            'after_discount': forms.NumberInput(attrs={'readonly': 'readonly'}),
        }

class PurchasePaidInvoiceForm(forms.ModelForm):
    class Meta:
        model = MagedInvoice
        exclude = ['customer_debit']
        fields = [
            'after_discount',
            'outgoing',
            'comment',
        ]
        labels = {
            'outgoing': 'مدفوع',
        }
        widgets = {
            'after_discount': forms.NumberInput(attrs={'readonly': 'readonly'}),
        }


class PlusMinusForm(forms.ModelForm):
    class Meta:
        model = MagedInvoice
        fields = [
            'comment',
            'internal_comment',
        ]

#
class QuotationForm(forms.ModelForm):
    class Meta:
        model = MagedInvoice
        fields = ['after_discount', 'comment', 'internal_comment']

#
class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = MagedInvoiceItems
        exclude = ['invoice', 'main_unit_quantity', 'main_unit_main_warehouse', 'main_unit_sub_warehouse']
        widgets = {
            'item': forms.Select(attrs={
                'required':'required',
            }),
            'unit_name': forms.Select(attrs={
                'required':'required',
            }),
            'quantity': forms.NumberInput(attrs={
                'onfocusin': "this.parentNode.className='w-25 p-3'",
                'onfocusout': "this.parentNode.className='w-auto p-3'",
                'required':'required',
            }),
            'unit_price': forms.NumberInput(attrs={
                'onfocusin': "this.parentNode.className='w-25 p-3'",
                'onfocusout': "this.parentNode.className='w-auto p-3'",
                'required':'required',
            }),
            'total_price': forms.NumberInput(attrs={
                'onfocusin': "this.parentNode.className='w-25 p-3'",
                'onfocusout': "this.parentNode.className='w-auto p-3'",
                'required':'required',
            }),
            'discount': forms.NumberInput(attrs={
                'onfocusin': "this.parentNode.className='w-25 p-3'",
                'onfocusout': "this.parentNode.className='w-auto p-3'",
            }),
            'after_discount': forms.NumberInput(attrs={
                'onfocusin': "this.parentNode.className='w-25 p-3'",
                'onfocusout': "this.parentNode.className='w-auto p-3'",
                'required':'required',
            }),
            'comment': forms.TextInput(attrs={
                'onfocusin': "this.parentNode.className='w-25 p-3'",
                'onfocusout': "this.parentNode.className='w-auto p-3'",
            }),
            'main_warehouse': forms.NumberInput(attrs={
                'onfocusin': "this.parentNode.className='w-25 p-3'",
                'onfocusout': "this.parentNode.className='w-auto p-3'",
                'required':'required',
            }),
            'sub_warehouse': forms.NumberInput(attrs={
                'onfocusin': "this.parentNode.className='w-25 p-3'",
                'onfocusout': "this.parentNode.className='w-auto p-3'",
            }),
        }
#
#
class InvoiceDeleteForm(forms.ModelForm):
    class Meta:
        model = MagedInvoice
        fields = ['deleted']
#
#
class InvoiceItemPriceUpdateForm(forms.ModelForm):
    class Meta:
        model = MagedInvoiceItems
        fields = ['unit_price']
#
#
class InvoiceItemQuantityUpdateForm(forms.ModelForm):
    class Meta:
        model = MagedInvoiceItems
        exclude = ['main_warehouse', 'sub_warehouse']
        fields = ['quantity']


class InvoiceItemMainWarehouseUpdateForm(forms.ModelForm):
    class Meta:
        model = MagedInvoiceItems
        exclude = ['sub_warehouse']
        fields = ['main_warehouse']


class InvoiceItemSubWarehouseUpdateForm(forms.ModelForm):
    class Meta:
        model = MagedInvoiceItems
        exclude = ['main_warehouse']
        fields = ['sub_warehouse']

#
#
class InvoiceItemDiscountUpdateForm(forms.ModelForm):
    class Meta:
        model = MagedInvoiceItems
        fields = ['discount']
#
#
class InvoiceDateForm(forms.ModelForm):
    class Meta:
        model = MagedInvoice
        fields = ['date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }
#
#
class InvoiceDiscountUpdateForm(forms.ModelForm):
    class Meta:
        model = MagedInvoice
        fields = ['discount']


class InvoiceCustomerForm(forms.ModelForm):
    class Meta:
        model = MagedInvoice
        fields = ['customer']
#
#
class InvoiceToBranchForm(forms.ModelForm):
    class Meta:
        model = MagedInvoice
        fields = ['branch']
#
#
class InvoiceFromBranchForm(forms.ModelForm):
    class Meta:
        model = MagedInvoice
        fields = ['branch']

class InvoiceFromTreasuryForm(forms.ModelForm):
    class Meta:
        model = MagedInvoice
        fields = ['treasury']


class InvoiceToTreasuryForm(forms.ModelForm):
    class Meta:
        model = MagedInvoice
        fields = ['treasury']

#
#
#
#
#
class InvoiceUnSaveForm(forms.ModelForm):
    class Meta:
        model = MagedInvoice
        fields = ['saved']
#
#
class ExpenseInvoiceForm(forms.ModelForm):
    class Meta:
        model = MagedInvoice
        fields = ['date', 'outgoing', 'treasury', 'comment']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }
        treasury = forms.ModelChoiceField(queryset=Treasury.objects.filter(deleted=False), label='الخزينة')
#
#
#
class IncomeInvoiceForm(forms.ModelForm):
    class Meta:
        model = MagedInvoice
        fields = ['date', 'outgoing', 'treasury', 'comment']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }
        treasury = forms.ModelChoiceField(queryset=Treasury.objects.filter(deleted=False), label='الخزينة')

#
class SettingForm(forms.ModelForm):
    class Meta:
        model = InvoiceSetting
        fields = '__all__'
#
#
class BaseSettingForm(forms.ModelForm):
    class Meta:
        model = InvoiceBaseSetting
        fields = '__all__'
#
#
# class CustomerOutcomeForm(forms.ModelForm):
#     class Meta:
#         model = MagedInvoice
#         fields = ['date', 'customer', 'outgoing', 'treasury',  'comment']
#         widgets = {
#             'date': forms.DateInput(attrs={'type': 'date'})
#         }
#
#
# class CustomerIncomeForm(forms.ModelForm):
#     class Meta:
#         model = MagedInvoice
#         fields = ['date', 'customer','incoming', 'treasury','comment']
#         widgets = {
#             'date': forms.DateInput(attrs={'type': 'date'})
#         }
#
#
class CapitalOutcomeForm(forms.ModelForm):
    class Meta:
        model = MagedInvoice
        fields = ['date', 'outgoing', 'treasury',  'comment']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }
#
#
class CapitalIncomeForm(forms.ModelForm):
    class Meta:
        model = MagedInvoice
        fields = ['date', 'outgoing', 'treasury',   'comment']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }
#
#
class BranchTransferForm(forms.ModelForm):
    class Meta:
        model = MagedInvoice
        fields = [
            'branch',
        ]
#
#
class StockTransferSaveForm(forms.ModelForm):
    class Meta:
        model = MagedInvoice
        fields = [
            'comment',
            'internal_comment',
        ]

#
class TreasuryTransferForm(forms.ModelForm):
    class Meta:
        model = MagedInvoice
        fields = [
            'date',
            'treasury',
            'comment',
        ]

        labels = {
            'incoming': 'المبلغ',
        }

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }
