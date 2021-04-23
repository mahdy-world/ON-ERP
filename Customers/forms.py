from django import forms


from .models import *


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ['deleted']


class CategoryDeleteForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['deleted']
        
        
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ['deleted', 'seller_feedback', 'accountant_notes', 'purchase_invoices_comments']
        widgets = {
            'added_by': forms.HiddenInput(),
            'address': forms.Textarea(attrs={'rows': '2'})
            # 'payments_status': forms.TextInput(attrs={'type': 'color'}),
            # 'Products_status': forms.TextInput(attrs={'type': 'color'}),
        }

class CustomerNotesForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['seller_feedback', 'accountant_notes', 'purchase_invoices_comments']
        exclude = ['deleted']
        widgets = {
            'seller_feedback': forms.Textarea(attrs={'rows': '3'}),
            'accountant_notes': forms.Textarea(attrs={'rows': '3'}),
            'purchase_invoices_comments': forms.Textarea(attrs={'rows': '3'})}




class CustomerEditForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ['deleted', 'added_by']


class CustomerDeleteForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['deleted']




class CallReasonForm(forms.ModelForm):
    class Meta:
        model = CallReason
        exclude = ['deleted']


class CallReasonDeleteForm(forms.ModelForm):
    class Meta:
        model = CallReason
        fields = ['deleted']


class CustomerCallForm(forms.ModelForm):
    class Meta:
        model = CustomerCall
        fields = ['call_type', 'call_reason', 'summary']



class CustomerTypeList(forms.ModelForm):
    class Meta:
        model = CustomerType
        fields = ['name']



class CustomerEditForm(forms.ModelForm):
    class Meta:
        model = CustomerType
        exclude = ['deleted', 'added_by']


class CustomerTypeEditForm(forms.ModelForm):
    class Meta:
        model = CustomerType
        exclude = ['deleted','added_by']
        

class CustomerTypeForm(forms.ModelForm):
    class Meta:
        model = CustomerType
        exclude = ['deleted']
        widgets = {
            'added_by' : forms.HiddenInput(),
        }

class CustomerTypeDeleteForm(forms.ModelForm):
    class Meta:
        model = CustomerType
        fields = ['deleted']