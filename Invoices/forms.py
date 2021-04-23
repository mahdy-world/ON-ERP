from django import forms

from .models import *


class SalesInvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'after_discount',
            'invoice_discount',
            'shipping',
            'internal_comment',
        ]
        widgets = {
            'after_discount': forms.NumberInput(attrs={'readonly': 'readonly'}),
        }

class SalesPaidInvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        exclude = ['customer_credit']
        fields = [
            'overall',
            'treasury_in',
            'comment',
        ]
        labels = {
            'treasury_in': 'مدفوع',
        }
        widgets = {
            'overall': forms.NumberInput(attrs={'readonly': 'readonly'}),
        }

class PurchaseInvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'after_discount',
            'invoice_discount',
            'shipping',
            'internal_comment',
        ]
        widgets = {
            'after_discount': forms.NumberInput(attrs={'readonly': 'readonly'}),
        }

class PurchasePaidInvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        exclude = ['customer_debit']
        fields = [
            'overall',
            'treasury_out',
            'comment',
        ]
        labels = {
            'treasury_out': 'مدفوع',
        }
        widgets = {
            'overall': forms.NumberInput(attrs={'readonly': 'readonly'}),
        }


class OutInvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'numbering',
        ]

class PlusMinusForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'comment',
            'internal_comment',
        ]


class QuotationForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['after_discount', 'comment', 'internal_comment']

class InvoiceItemForm2(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        exclude = ['invoice']
        fields = ['item', 'quantity', 'unit_name', 'comment']


class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        exclude = ['invoice', 'profit', 'main_unit_quantity', 'main_unit_main_warehouse', 'main_unit_sub_warehouse']
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
            'main_unit_price': forms.NumberInput(attrs={
                'onfocusin': "this.parentNode.className='w-25 p-3'",
                'onfocusout': "this.parentNode.className='w-auto p-3'",
                'required': 'required',
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


class InvoiceDeleteForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['deleted']


class InvoiceItemPriceUpdateForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['unit_price']

class InvoiceItemMainPriceUpdateForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['main_unit_price']

class InvoiceItemQuantityUpdateForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        exclude = ['main_warehouse', 'sub_warehouse']
        fields = ['quantity']


class InvoiceItemMainWarehouseUpdateForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        exclude = ['sub_warehouse']
        fields = ['main_warehouse']


class InvoiceItemSubWarehouseUpdateForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        exclude = ['main_warehouse']
        fields = ['sub_warehouse']


class InvoiceItemDiscountUpdateForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['discount']


class InvoiceDateForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }


class InvoiceDiscountUpdateForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['discount']


class InvoiceCustomerForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['customer']


class InvoiceToBranchForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['to_branch']


class InvoiceFromBranchForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['from_branch']


class InvoiceFromMainWarehouseForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['main_warehouse']


class InvoiceFromSubWarehouseForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['sub_warehouse']


class InvoiceFromTreasuryForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['from_treasury']


class InvoiceToTreasuryForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['to_treasury']


class InvoiceUnSaveForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['saved']


class ExpenseInvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['date', 'spend_category', 'treasury_out', 'from_treasury', 'comment']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }
        spend_category = forms.ModelChoiceField(queryset=SpendCategory.objects.filter(deleted=False), label='تصنيف المصروفات')
        from_treasury = forms.ModelChoiceField(queryset=Treasury.objects.filter(deleted=False), label='من خزينة')



class IncomeInvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['date', 'spend_category', 'treasury_in', 'to_treasury', 'comment']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }
        spend_category = forms.ModelChoiceField(queryset=SpendCategory.objects.filter(deleted=False), label='تصنيف القبض')
        to_treasury = forms.ModelChoiceField(queryset=Treasury.objects.filter(deleted=False), label='إلي خزينة')

class SettingForm(forms.ModelForm):
    class Meta:
        model = InvoiceSetting
        fields = '__all__'


class BaseSettingForm(forms.ModelForm):
    class Meta:
        model = InvoiceBaseSetting
        fields = '__all__'


class CustomerOutcomeForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['date', 'customer', 'treasury_out', 'from_treasury',  'comment']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }


class CustomerIncomeForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['date', 'customer','treasury_in', 'to_treasury','comment']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }


class CapitalOutcomeForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['date', 'partner','treasury_out', 'from_treasury',  'comment']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }


class CapitalIncomeForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['date', 'partner', 'treasury_in', 'to_treasury',   'comment']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }


class SpendCategoryForm(forms.ModelForm):
    class Meta:
        model = SpendCategory
        exclude = ['deleted']


class SpendCategoryDeleteForm(forms.ModelForm):
    class Meta:
        model = SpendCategory
        fields = ['deleted']


class BranchTransferForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'from_branch',
            'to_branch',
        ]

class WarehouseTransferForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'from_warehouse',
            'to_warehouse',
        ]

class StockTransferSaveForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'comment',
            'internal_comment',
        ]


class TreasuryTransferForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'date',
            'from_treasury',
            'to_treasury',
            'treasury_in',
            'comment',
        ]

        labels = {
            'treasury_in': 'المبلغ',
        }
        
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }
