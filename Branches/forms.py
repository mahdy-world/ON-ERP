from django import forms
from .models import *



#Branch Form
class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        exclude = ['deleted']

class BranchDeleteForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['deleted']


#Warehouse Form
class WarehouseDeleteForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ['deleted']


class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        exclude = ['deleted']


class BranchWarehousesForm(forms.ModelForm):
    class Meta:
        model = BranchWarehouses
        fields = ['main_warehouse' , 'sub_warehouse']
        
