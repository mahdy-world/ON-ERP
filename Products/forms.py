from django import forms
from .models import *


class MainCategoryForm(forms.ModelForm):
    class Meta:
        model = MainCategory
        exclude = ['deleted']


class MainCategoryDeleteForm(forms.ModelForm):
    class Meta:
        model = MainCategory
        fields = ['deleted']


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        exclude = ['deleted']


class SubCategoryDeleteForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['deleted']
        

class ManufactureForm(forms.ModelForm):
    class Meta:
        model = Manufacture
        exclude = ['deleted']


class ManufactureDeleteForm(forms.ModelForm):
    class Meta:
        model = Manufacture
        fields = ['deleted']
        

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        exclude = ['deleted']


class BrandDeleteForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['deleted']
        

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        exclude = ['deleted']


class UnitDeleteForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['deleted']
        

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['deleted', 'product_card_comment', 'supplier_comment', 'print_comment','initial_value', 'initial_branch', 'cost_price','purchase_price_new', 'purchase_price_new_activation', 
        'purchase_price_new_comment']
        widgets = {'description': forms.Textarea(attrs={'rows': '3'})}

class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['deleted', 'product_card_comment', 'supplier_comment', 'print_comment', 'sell_price', 'cost_price', 
        'purchase_price', 'initial_value', 'initial_branch','purchase_price_new', 'purchase_price_new_activation', 
        'purchase_price_new_comment','price_list']
        widgets = {'description': forms.Textarea(attrs={'rows': '3'})}

class ProductNoteForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_card_comment', 'supplier_comment', 'print_comment']
        widgets = {'product_card_comment': forms.Textarea(attrs={'rows': '3'}),'supplier_comment': forms.Textarea(attrs={'rows': '3'}),'print_comment': forms.Textarea(attrs={'rows': '3'})}


class ProductDeleteForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['deleted']


class GroupedProductForm(forms.ModelForm):
    class Meta:
        model = GroupedProduct
        exclude = ['grouped_item']

#############################

class PricesProductForm(forms.ModelForm):
    class Meta:
        model = ProductPrices
        exclude = ['product']
        fields = ['customer_segment', 'price']

class PricesProductFormU(forms.ModelForm):
    class Meta:
        model = ProductPrices
        fields = ['price', 'discount', 'opration', 'order']

class PricesProductFormD(forms.ModelForm):
    class Meta:
        model = ProductPrices
        fields = ['deleted']

class PricesProductFormS(forms.ModelForm):
    class Meta:
        model = ProductPrices
        fields = ['inactive']

class ProductPriceForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['price_list','sell_price', 'purchase_price', 'purchase_price_new', 'purchase_price_new_activation', 'purchase_price_new_comment']
        widgets = {'purchase_price_new_comment': forms.Textarea(attrs={'rows': '3'})}


class MainPriceListForm(forms.ModelForm):
    class Meta:
        model = PricesList
        exclude = ['deleted']

class MainPriceListDeleteForm(forms.ModelForm):
    class Meta:
        model = PricesList
        fields = ['deleted']


class UnitsProductForm(forms.ModelForm):
    class Meta:
        model = ProductUnit
        exclude = ['product']
        fields = ['unit_name', 'unit_quantity', 'unit_from', 'sell_price_factor', 'purchase_price_factor']

class UnitsProductFormD(forms.ModelForm):
    class Meta:
        model = ProductUnit
        fields = ['deleted']

class CustomerPricesUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomerPrices
        exclude = ['deleted']

class CustomerPricesDeleteForm(forms.ModelForm):
    class Meta:
        model = CustomerPrices
        fields = ['deleted']