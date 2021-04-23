from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import *
from django.urls import reverse_lazy

from Customers.models import Category
from Branches.models import BranchWarehouses
from Invoices.models import WarehouseTransactions
from .models import *
from .forms import *
from django.db.models import Q


# Create your views here.
class MainCategoryList(ListView):
    model = MainCategory
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        return queryset


class MainCategoryTrashList(ListView):
    model = MainCategory
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        return queryset


class MainCategoryCreate(CreateView):
    model = MainCategory
    form_class = MainCategoryForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Products:MainCategoryList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة مجموعة أصناف رئيسية'
        context['action_url'] = reverse_lazy('Products:MainCategoryCreate')
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class MainCategoryUpdate(UpdateView):
    model = MainCategory
    form_class = MainCategoryForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Products:MainCategoryList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل مجموعة أصناف رئيسية: ' + str(self.object)
        context['action_url'] = reverse_lazy('Products:MainCategoryUpdate', kwargs={'pk': self.object.id})
        return context


class MainCategoryDelete(UpdateView):
    model = MainCategory
    form_class = MainCategoryDeleteForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Products:MainCategoryList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل مجموعة أصناف رئيسية: ' + str(self.object)
        context['action_url'] = reverse_lazy('Products:MainCategoryDelete', kwargs={'pk': self.object.id})
        return context
    

class SubCategoryList(ListView):
    model = SubCategory
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        if self.request.GET.get('main_category'):
            queryset = queryset.filter(main_category__name__icontains=self.request.GET.get('main_category'))
        return queryset


class SubCategoryTrashList(ListView):
    model = SubCategory
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        if self.request.GET.get('main_category'):
            queryset = queryset.filter(main_category__name__icontains=self.request.GET.get('main_category'))
        return queryset


class SubCategoryCreate(CreateView):
    model = SubCategory
    form_class = SubCategoryForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Products:SubCategoryList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة مجموعة أصناف فرعية'
        context['action_url'] = reverse_lazy('Products:SubCategoryCreate')
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class SubCategoryUpdate(UpdateView):
    model = SubCategory
    form_class = SubCategoryForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Products:SubCategoryList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل مجموعة أصناف فرعية: ' + str(self.object)
        context['action_url'] = reverse_lazy('Products:SubCategoryUpdate', kwargs={'pk': self.object.id})
        return context


class SubCategoryDelete(UpdateView):
    model = SubCategory
    form_class = SubCategoryDeleteForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Products:SubCategoryList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل مجموعة أصناف فرعية: ' + str(self.object)
        context['action_url'] = reverse_lazy('Products:SubCategoryDelete', kwargs={'pk': self.object.id})
        return context
    
    
class ManufactureList(ListView):
    model = Manufacture
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        return queryset


class ManufactureTrashList(ListView):
    model = Manufacture
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        return queryset


class ManufactureCreate(CreateView):
    model = Manufacture
    form_class = ManufactureForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Products:ManufactureList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة شركة مصنعة'
        context['action_url'] = reverse_lazy('Products:ManufactureCreate')
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class ManufactureUpdate(UpdateView):
    model = Manufacture
    form_class = ManufactureForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Products:ManufactureList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل شركة مصنعة: ' + str(self.object)
        context['action_url'] = reverse_lazy('Products:ManufactureUpdate', kwargs={'pk': self.object.id})
        return context


class ManufactureDelete(UpdateView):
    model = Manufacture
    form_class = ManufactureDeleteForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Products:ManufactureList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل شركة مصنعة: ' + str(self.object)
        context['action_url'] = reverse_lazy('Products:ManufactureDelete', kwargs={'pk': self.object.id})
        return context


class BrandList(ListView):
    model = Brand
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        return queryset


class BrandTrashList(ListView):
    model = Brand
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        return queryset


class BrandCreate(CreateView):
    model = Brand
    form_class = BrandForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Products:BrandList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة براند'
        context['action_url'] = reverse_lazy('Products:BrandCreate')
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class BrandUpdate(UpdateView):
    model = Brand
    form_class = BrandForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Products:BrandList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل براند: ' + str(self.object)
        context['action_url'] = reverse_lazy('Products:BrandUpdate', kwargs={'pk': self.object.id})
        return context


class BrandDelete(UpdateView):
    model = Brand
    form_class = BrandDeleteForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Products:BrandList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل براند: ' + str(self.object)
        context['action_url'] = reverse_lazy('Products:BrandDelete', kwargs={'pk': self.object.id})
        return context


class UnitList(ListView):
    model = Unit
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        return queryset


class UnitCreate(CreateView):
    model = Unit
    form_class = UnitForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Products:UnitList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة وحدة'
        context['action_url'] = reverse_lazy('Products:UnitCreate')
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

class UnitTrashList(ListView):
    model = Unit
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        return queryset


class UnitUpdate(UpdateView):
    model = Unit
    form_class = UnitForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Products:UnitList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل وحدة: ' + str(self.object)
        context['action_url'] = reverse_lazy('Products:UnitUpdate', kwargs={'pk': self.object.id})
        return context


class UnitDelete(UpdateView):
    model = Unit
    form_class = UnitDeleteForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Products:UnitList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل وحدة: ' + str(self.object)
        context['action_url'] = reverse_lazy('Products:UnitDelete', kwargs={'pk': self.object.id})
        return context


class ProductList(ListView):
    model = Product
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        if self.request.GET.get('description'):
            queryset = queryset.filter(description__icontains=self.request.GET.get('description'))
        if self.request.GET.get('main_category'):
            queryset = queryset.filter(sub_category__main_category__name__icontains=self.request.GET.get('main_category'))
        if self.request.GET.get('sub_category'):
            queryset = queryset.filter(sub_category__name__icontains=self.request.GET.get('sub_category'))
        if self.request.GET.get('manufacture'):
            queryset = queryset.filter(manufacture__name__icontains=self.request.GET.get('manufacture'))
        if self.request.GET.get('brand'):
            queryset = queryset.filter(brand__name__icontains=self.request.GET.get('brand'))
        if self.request.GET.get('purchase_price'):
            queryset = queryset.filter(purchase_price=self.request.GET.get('purchase_price'))
        if self.request.GET.get('cost_price'):
            queryset = queryset.filter(cost_price=self.request.GET.get('cost_price'))
        if self.request.GET.get('sell_price'):
            queryset = queryset.filter(sell_price=self.request.GET.get('sell_price'))
        if self.request.GET.get('main_unit'):
            queryset = queryset.filter(main_unit__name__icontains=self.request.GET.get('main_unit'))
        if self.request.GET.get('sub_unit'):
            queryset = queryset.filter(sub_unit__name__icontains=self.request.GET.get('sub_unit'))
        if self.request.GET.get('sub_sub_unit'):
            queryset = queryset.filter(sub_sub_unit__name__icontains=self.request.GET.get('sub_sub_unit'))
        return queryset


class ProductCreate(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Products:ProductList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة صنف'
        context['action_url'] = reverse_lazy('Products:ProductCreate')
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


def product_create(request):
    form = ProductForm(request.POST or None)
    form2 = ProductNoteForm(request.POST or None)
    title = 'إضافة صنف'

    if form.is_valid():
        product = form.save()

        if product.price_list == 'None':
            for x in Category.objects.filter(deleted = False):
                product_price = ProductPrices()
                product_price.product = product
                product_price.customer_segment = x
                product_price.price = product.sell_price
                product_price.discount = 0
                product_price.new_price = product.sell_price
                product_price.save()
        else:
            price_list = PricesList.objects.get(name = product.price_list)
            for x in CustomerPrices.objects.filter(deleted = False, prices_list = price_list ):
                product_price = ProductPrices()
                product_price.product = product
                product_price.customer_segment = x.customer_segment
                product_price.price = product.sell_price
                product_price.discount = x.discount
                product_price.opration = x.opration

                if str(price_list.opration) == '1':
                    product_price.new_price = (product.sell_price - (price_list.percentage * product.sell_price /100 ))
                if str(price_list.opration) == '2':
                    product_price.new_price = (product.sell_price + (price_list.percentage * product.sell_price /100 ))

                product_price.save()

        form2.save(commit=False)
        x = Product.objects.get(id = product.id)
        x.product_card_comment = form2.instance.product_card_comment
        x.supplier_comment = form2.instance.supplier_comment
        x.print_comment = form2.instance.print_comment
        x.save()
        return redirect('Products:ProductCard', product.id)
    context = {
        'form': form,
        'title': title,
        'form2' : form2,
    }
    return render(request, 'Core/form_template.html', context)


class ProductUpdate(UpdateView):
    model = Product
    form_class = ProductUpdateForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Products:ProductList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل صنف: ' + str(self.object)
        context['action_url'] = reverse_lazy('Products:ProductUpdate', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        prod_old = Product.objects.get(id=self.object.id)
        """
        Overridden to add the ipsum relation to the `Lorem` instance.
        """
        ware = form.save(commit=False)
        # if prod_old.purchase_price != ware.purchase_price or prod_old.initial_value != ware.initial_value:
        #     warehouse = None
        #     if ware.initial_branch and BranchWarehouses.objects.filter(branch=ware.initial_branch):
        #         warehouse = BranchWarehouses.objects.get(branch=ware.initial_branch)
        #
        #     warehouse_transactions0 = WarehouseTransactions.objects.filter(item=self.object.id, warehouse=warehouse.main_warehouse).first()
        #     warehouse_transactions0.delete()
        #     warehouse_transactions = WarehouseTransactions()
        #     warehouse_transactions.warehouse = warehouse.main_warehouse
        #     warehouse_transactions.item = ware
        #     warehouse_transactions.incoming = ware.initial_value
        #     warehouse_transactions.purchase_cost = ware.purchase_price
        #     warehouse_transactions.total_incoming = ware.initial_value * ware.purchase_price
        #     warehouse_transactions.balance = ware.initial_value
        #     warehouse_transactions.save()
        return super().form_valid(form)


class ProductNoteUpdate(UpdateView):
    model = Product
    form_class = ProductNoteForm
    template_name = 'Core/form_template.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة ملاحظات للصنف: ' + str(self.object)
        context['action_url'] = reverse_lazy('Products:ProductUpdate', kwargs={'pk': self.object.id})
        return context
    def get_success_url(self):
        return reverse_lazy('Products:ProductCard', kwargs={'pk': self.object.pk})


class ProductDelete(UpdateView):
    model = Product
    form_class = ProductDeleteForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Products:ProductList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف صنف: ' + str(self.object)
        context['action_url'] = reverse_lazy('Products:ProductDelete', kwargs={'pk': self.object.id})
        return context


class ProductCard(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        product_item = get_object_or_404(Product, id=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)

        # units = {}
        # product_units = ProductUnit.objects.filter(product=product_item, deleted=0)

        # if product_item.main_unit != None:
        #     for unit in product_units:
        #         if unit.unit_from == product_item.main_unit:
        #             result = float(unit.unit_quantity)
        #             units[unit.id] = result
        #         else:
        #             if product_units.filter(unit_name=unit.unit_from):
        #                 un = product_units.get(unit_name=unit.unit_from)
        #                 uu = units[un.id]
        #                 result = float(unit.unit_quantity) * uu
        #                 units[unit.id] = result
        #             else:

        #                 result = float(unit.unit_quantity)
        #                 units[unit.id] = result

        units = {}
        units_1 = []
        u = 1.0
        y = 1.0
        product_units_1 = ProductUnit.objects.filter(Q(unit_name=product_item.main_unit) | Q(unit_from=product_item.main_unit), product=product_item, deleted=0)
        product_units_2 = ProductUnit.objects.filter(~Q(unit_name=product_item.main_unit), ~Q(unit_from=product_item.main_unit), product=product_item, deleted=0)
        product_units_all = ProductUnit.objects.filter(product=product_item, deleted=0)

        if product_item.main_unit != None:
            for unit1 in product_units_1:
                result = float(unit1.unit_quantity)
                units[unit1.id] = result
                units_1.append(result)

            for i in units_1:
                u *= i

            for x in product_units_all:
                y *= x.unit_quantity

            for unit2 in product_units_2:
                if product_units_2.filter(unit_name=unit2.unit_from).exists()==False:
                    if unit2.unit_from != None:
                        result = float(unit2.unit_quantity) * u
                        units[unit2.id] = result
                    else:
                        result = y
                        units[unit2.id] = result
                else:
                    un = product_units_2.get(unit_name=unit2.unit_from)
                    uu = units[un.id]
                    result = float(unit2.unit_quantity) * uu
                    units[unit2.id] = result


        context['prod_units'] = units
        context['actions'] = ProductActions.objects.filter(product=product_item)
        context['units'] = ProductUnit.objects.filter(product=product_item, deleted=0).order_by('id')
        context['action_url'] = reverse_lazy('Products:ProductCard', kwargs={'pk': self.object.id})
        return context


class GroupedProductCreate(CreateView):
    model = GroupedProduct
    template_name = 'Core/form_template.html'
    form_class = GroupedProductForm

    def form_valid(self, form):
        """
        Overridden to add the ipsum relation to the `Lorem` instance.
        """
        grouped_item = get_object_or_404(Product, id=self.kwargs['pk'])
        form.instance.grouped_item = grouped_item
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة مكونات: ' + str(self.object)
        context['action_url'] = reverse_lazy('Products:GroupedProductCreate', kwargs={'pk': self.kwargs['pk']})
        return context
    def get_success_url(self):
        return reverse_lazy('Products:ProductCard', kwargs={'pk': self.kwargs['pk'] })



class GroupedProductUpdate(UpdateView):
    model = GroupedProduct
    template_name = 'Core/form_template.html'
    form_class = GroupedProductForm

    def form_valid(self, form):
        """
        Overridden to add the ipsum relation to the `Lorem` instance.
        """
        grouped_item = get_object_or_404(Product, id=self.kwargs['ppk'])
        form.instance.grouped_item = grouped_item
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل مكونات: ' + str(self.object)
        context['action_url'] = reverse_lazy('Products:GroupedProductUpdate', kwargs={'pk': self.kwargs['pk']})
        return context
    def get_success_url(self):
        return reverse_lazy('Products:ProductCard', kwargs={'pk': self.kwargs['ppk'] })



class GroupedProductDelete(DeleteView):
    model = GroupedProduct
    form_class = GroupedProductForm
    template_name = 'Core/form_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف مكونات: ' + str(self.object)
        context['action_url'] = reverse_lazy('Products:GroupedProductDelete', kwargs={'pk': self.kwargs['pk']})
        return context
    def get_success_url(self):
        return reverse_lazy('Products:ProductCard', kwargs={'pk': self.kwargs['ppk'] })


class ProductTrashList(ListView):
    model = Product
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        if self.request.GET.get('description'):
            queryset = queryset.filter(description__icontains=self.request.GET.get('description'))
        if self.request.GET.get('main_category'):
            queryset = queryset.filter(sub_category__main_category__name__icontains=self.request.GET.get('main_category'))
        if self.request.GET.get('sub_category'):
            queryset = queryset.filter(sub_category__name__icontains=self.request.GET.get('sub_category'))
        if self.request.GET.get('manufacture'):
            queryset = queryset.filter(manufacture__name__icontains=self.request.GET.get('manufacture'))
        if self.request.GET.get('brand'):
            queryset = queryset.filter(brand__name__icontains=self.request.GET.get('brand'))
        if self.request.GET.get('purchase_price'):
            queryset = queryset.filter(purchase_price=self.request.GET.get('purchase_price'))
        if self.request.GET.get('cost_price'):
            queryset = queryset.filter(cost_price=self.request.GET.get('cost_price'))
        if self.request.GET.get('sell_price'):
            queryset = queryset.filter(sell_price=self.request.GET.get('sell_price'))
        if self.request.GET.get('main_unit'):
            queryset = queryset.filter(main_unit__name__icontains=self.request.GET.get('main_unit'))
        if self.request.GET.get('sub_unit'):
            queryset = queryset.filter(sub_unit__name__icontains=self.request.GET.get('sub_unit'))
        if self.request.GET.get('sub_sub_unit'):
            queryset = queryset.filter(sub_sub_unit__name__icontains=self.request.GET.get('sub_sub_unit'))
        return queryset

################################################

class PricesProductCreate(CreateView):
    model = ProductPrices
    template_name = 'Core/form_template.html'
    form_class = PricesProductForm
    success_url = reverse_lazy('Products:ProductList')

    def form_valid(self, form):
        """
        Overridden to add the ipsum relation to the `Lorem` instance.
        """
        prices_item = get_object_or_404(Product, id=self.kwargs['pk'])
        form.instance.product = prices_item
        category_item = get_object_or_404(Category, id=int(self.request.POST.get('customer_segment')))
        action = ProductActions()
        action.product = prices_item
        action.action_userid = self.request.user
        action.action_type = 'اضافة سعر شريحة'
        action.action_name = category_item.name
        action.action_from = 0.0
        action.action_to = float(self.request.POST.get('price'))
        action.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        product_item = get_object_or_404(Product, id=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة سعر شريحة: ' + str(product_item.name)
        context['action_url'] = reverse_lazy('Products:PricesProductCreate', kwargs={'pk': self.kwargs['pk']})
        return context

class PricesProductUpdate(UpdateView):
    model = ProductPrices
    template_name = 'Core/form_template.html'
    form_class = PricesProductFormU

    def form_valid(self, form):
        x = form.save(commit=False)
        if x.opration == '1':
            x.new_price = x.price - (x.discount * x.price / 100)
        else:
            x.new_price = x.price + (x.discount * x.price / 100)
        x.save()
        
        product_item = get_object_or_404(ProductPrices, id=self.kwargs['pk'])
        action = ProductActions()
        action.product = product_item.product
        action.action_userid = self.request.user
        action.action_type = 'تعديل سعر شريحة: '
        action.action_name = product_item.customer_segment.name
        action.action_from = product_item.price
        action.action_to = float(self.request.POST.get('price'))
        action.save()
        return super(PricesProductUpdate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل الشريحة: ' + str(self.object)
        context['action_url'] = reverse_lazy('Products:PricesProductUpdate', kwargs={'pk': self.kwargs['pk']})
        return context
    def get_success_url(self):
        return reverse_lazy('Products:ProductCard', kwargs={'pk': self.kwargs['ppk'] })


class PricesProductDelete(UpdateView):
    model = ProductPrices
    template_name = 'Core/confirm_delete.html'
    form_class = PricesProductFormD

    def form_valid(self, form):
        form.instance.deleted = 1
        product_item = get_object_or_404(ProductPrices, id=self.kwargs['pk'])
        action = ProductActions()
        action.product = product_item.product
        action.action_userid = self.request.user
        action.action_type = 'حذف سعر شريحة'
        action.action_name = product_item.customer_segment.name
        action.action_from = ''
        action.action_to = ''
        action.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف سعر شريحة: ' + str(self.object)
        context['action_url'] = reverse_lazy('Products:PricesProductDelete', kwargs={'pk': self.kwargs['pk']})
        return context
    def get_success_url(self):
        return reverse_lazy('Products:ProductCard', kwargs={'pk': self.kwargs['ppk'] })

class PricesProductStop(UpdateView):
    model = ProductPrices
    template_name = 'Core/confirm_stop.html'
    form_class = PricesProductFormS
    success_url = reverse_lazy('Products:ProductList')

    def form_valid(self, form):
        """
        Overridden to add the ipsum relation to the `Lorem` instance.
        """
        form.instance.inactive = 1
        product_item = get_object_or_404(ProductPrices, id=self.kwargs['pk'])
        action = ProductActions()
        action.product = product_item.product
        action.action_userid = self.request.user
        action.action_type = 'تعطيل سعر شريحة'
        action.action_name = product_item.customer_segment.name
        action.action_from = ''
        action.action_to = ''
        action.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعطيل سعر شريحة: ' + str(self.object)
        context['action_url'] = reverse_lazy('Products:PricesProductStop', kwargs={'pk': self.kwargs['pk']})
        return context

class PricesProductActive(UpdateView):
    model = ProductPrices
    template_name = 'Core/confirm_active.html'
    form_class = PricesProductFormS
    success_url = reverse_lazy('Products:ProductList')

    def form_valid(self, form):
        """
        Overridden to add the ipsum relation to the `Lorem` instance.
        """
        form.instance.inactive = 0
        product_item = get_object_or_404(ProductPrices, id=self.kwargs['pk'])
        action = ProductActions()
        action.product = product_item.product
        action.action_userid = self.request.user
        action.action_type = 'تفعيل سعر شريحة'
        action.action_name = product_item.customer_segment.name
        action.action_from = ''
        action.action_to = ''
        action.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تفعيل سعر شريحة: ' + str(self.object)
        context['action_url'] = reverse_lazy('Products:PricesProductActive', kwargs={'pk': self.kwargs['pk']})
        return context

def PricesProductEditAll(request):
    new_prices_value = request.POST.get('new_prices_value')[:-1].split(',')
    for segment in new_prices_value:
        seg = segment.split('-')
        model = ProductPrices.objects.get(id=int(seg[0]))
        model.price = float(seg[1])
        model.save()
    return redirect('Products:ProductList')

class ProductPriceUpdate(UpdateView):
    model = Product
    form_class = ProductPriceForm
    template_name = 'Core/form_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل اسعار صنف: ' + str(self.object)
        context['action_url'] = reverse_lazy('Products:ProductPriceUpdate', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        product_item = get_object_or_404(Product, id=self.kwargs['pk'])

        if (form.instance.purchase_price_new_activation == True ) and (product_item.purchase_price_new != form.instance.purchase_price_new):
            for ProductPrice in ProductPrices.objects.filter(product=product_item):
                d = ProductPrice.new_price - product_item.purchase_price 
                ProductPrice.new_price = form.instance.purchase_price_new + d
                ProductPrice.save()
        else:
            if str(form.instance.price_list)  == 'None':
                for ProductPrice in ProductPrices.objects.filter(product=product_item):
                    new_price = self.request.POST.get('sell_price')
                    ProductPrice.price = self.request.POST.get('sell_price')
                    if str(ProductPrice.opration) == '1':
                        ProductPrice.new_price = float(float(new_price) - ((float(ProductPrice.discount) * float(new_price)) /100.0 ))
                    if str(ProductPrice.opration) == '2':
                        ProductPrice.new_price = float(float(new_price) + ((float(ProductPrice.discount) * float(new_price)) /100.0 ))
                    ProductPrice.save()
            else:
                if str(form.instance.price_list) != str(product_item.price_list):
                    price_list = PricesList.objects.get(name = form.instance.price_list)
                    for m in ProductPrices.objects.filter(product = product_item ):
                        m.delete()
                    for x in CustomerPrices.objects.filter(deleted = False, prices_list = price_list ):
                        product_price = ProductPrices()
                        product_price.product = product_item
                        product_price.customer_segment = x.customer_segment
                        product_price.price = product_item.sell_price
                        product_price.discount = x.discount
                        product_price.opration = x.opration
                        if str(x.opration) == '1':
                            product_price.new_price = (product_item.sell_price - (x.discount * product_item.sell_price /100 ))
                        if str(x.opration) == '2':
                            product_price.new_price = (product_item.sell_price + (x.discount * product_item.sell_price /100 ))
                        product_price.save()


        if str(self.request.POST.get('sell_price')) != str(product_item.sell_price):
                action = ProductActions()
                action.product = product_item
                action.action_userid = self.request.user
                action.action_type = 'تعديل سعر البيع الرئيسي'
                action.action_name = product_item.name
                action.action_from = product_item.sell_price
                action.action_to = float(self.request.POST.get('sell_price'))
                action.save()
        if str(self.request.POST.get('purchase_price')) != str(product_item.purchase_price):
                action = ProductActions()
                action.product = product_item
                action.action_userid = self.request.user
                action.action_type = 'تعديل سعر الشراء الرئيسي'
                action.action_name = product_item.name
                action.action_from = product_item.purchase_price
                action.action_to = float(self.request.POST.get('purchase_price'))
                action.save()
        
        return super(ProductPriceUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('Products:ProductCard', kwargs={'pk': self.kwargs['pk'] })



class MainPricesList(ListView):
    model = PricesList
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        return queryset


class MainPricesTrashList(ListView):
    model = PricesList
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        return queryset


class MainPricesListCreate(CreateView):
    model = PricesList
    form_class = MainPriceListForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Products:MainPricesList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة قائمة أسعار'
        context['action_url'] = reverse_lazy('Products:MainPricesListCreate')
        return context

    def form_valid(self, form):
        form.save()
        customers_segment = Category.objects.all()
        P_list = PricesList.objects.get(id = form.instance.id)
        for customer_segment in customers_segment:
           p = CustomerPrices(prices_list= P_list , customer_segment= customer_segment)
           p.save()
        return super().form_valid(form)

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class MainPricesListUpdate(UpdateView):
    model = PricesList
    form_class = MainPriceListForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Products:MainPricesList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل قائمة أسعار: ' + str(self.object)
        context['action_url'] = reverse_lazy('Products:MainPricesListUpdate', kwargs={'pk': self.object.id})
        return context


class MainPricesListDelete(UpdateView):
    model = PricesList
    form_class = MainPriceListDeleteForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Products:MainPricesList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف قائمة أسعار: ' + str(self.object)
        context['action_url'] = reverse_lazy('Products:MainPricesListDelete', kwargs={'pk': self.object.id})
        return context


class PricesListCard(DetailView):
    model = PricesList

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products_list'] = Product.objects.filter(deleted=0, price_list__id=self.object.id)
        context['CustomerPrices_list'] = CustomerPrices.objects.filter(deleted=0, prices_list=self.object)
        context['category_list'] = ProductPrices.objects.filter(deleted=0, product__price_list__id=self.object.id).values('customer_segment__id','customer_segment__name').distinct()
        context['action_url'] = reverse_lazy('Products:PricesListCard', kwargs={'pk': self.object.id})
        return context


def PricesProductListEditAll(request):
    new_prices_list = request.POST.get('new_prices_list').split(',')
    for list in new_prices_list:
        li = list.split('-')
        # ['1', '1', 'plus', '10', 'value', 'prod']
        products = Product.objects.filter(price_list__id=li[0])
        for product in products:
            segments = ProductPrices.objects.filter(product__id=product.id)
            for segment in segments:
                if segment.customer_segment.id == int(li[1]):
                    model = ProductPrices.objects.get(id=int(segment.id))
                    if li[2] == 'plus' and li[4] == 'value':
                        if li[5] == 'prod':
                            prod_price = float(model.product.sell_price)
                            model.price = prod_price + float(li[3])
                        if li[5] == 'segm':
                            segm_price = float(model.price)
                            model.price = segm_price + float(li[3])

                    elif li[2] == 'minus' and li[4] == 'value':
                        if li[5] == 'prod':
                            prod_price = float(model.product.sell_price)
                            model.price = prod_price - float(li[3])
                        if li[5] == 'segm':
                            segm_price = float(model.price)
                            model.price = segm_price - float(li[3])

                    elif li[2] == 'plus' and li[4] == 'rate':
                        if li[5] == 'prod':
                            prod_price = float(model.product.sell_price)
                            model.price = prod_price + (prod_price * float(li[3]) / 100)
                        if li[5] == 'segm':
                            segm_price = float(model.price)
                            model.price = segm_price + (segm_price * float(li[3]) / 100)

                    elif li[2] == 'minus' and li[4] == 'rate':
                        if li[5] == 'prod':
                            prod_price = float(model.product.sell_price)
                            model.price = prod_price - (prod_price * float(li[3]) / 100)
                        if li[5] == 'segm':
                            segm_price = float(model.price)
                            model.price = segm_price - (segm_price * float(li[3]) / 100)

                    model.save()

    return redirect('Products:MainPricesList')


class ProductUnitCreate(CreateView):
    model = ProductUnit
    template_name = 'Core/form_template.html'
    form_class = UnitsProductForm
    success_url = reverse_lazy('Products:ProductList')

    def form_valid(self, form):
        """
        Overridden to add the ipsum relation to the `Lorem` instance.
        """
        product_item = get_object_or_404(Product, id=self.kwargs['pk'])
        product_unit = ProductUnit.objects.filter(product=product_item)
        form.instance.product = product_item
        if self.request.POST.get('unit_name') and self.request.POST.get('unit_from') and self.request.POST.get('unit_name') != self.request.POST.get('unit_from'):
            # if self.request.POST.get('unit_from') == product_item.main_unit and product_unit.count() == 0:
            return super().form_valid(form)
            # elif product_unit.filter(unit_from__name__icontains=product_item.main_unit.name):
            #     return super().form_valid(form)
            # else:
            #     return redirect('Products:ProductCard', pk=self.kwargs['pk'])
        else:
            return redirect('Products:ProductCard', pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        product_item = get_object_or_404(Product, id=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة وحدة منتج: ' + str(product_item.name)
        context['action_url'] = reverse_lazy('Products:ProductUnitCreate', kwargs={'pk': self.kwargs['pk']})
        # form = self.form_class(self.request.POST or None)
        # form.fields['unit_from'].queryset = Unit.objects.filter(deleted=False)
        # context['form'] = form
        return context

    def get_form(self, *args, **kwargs):
        product_item = get_object_or_404(Product, id=self.kwargs['pk'])
        form = super(ProductUnitCreate, self).get_form(*args, **kwargs)
        form.fields['unit_from'].queryset = Unit.objects.filter(deleted=False)
        form.fields['unit_name'].queryset = Unit.objects.filter(~Q(name=product_item.main_unit), deleted=False)
        form.fields['unit_from'].initial = Unit.objects.get(id=product_item.main_unit.id)
        return form


class ProductUnitUpdate(UpdateView):
    model = ProductUnit
    template_name = 'Core/form_template.html'
    form_class = UnitsProductForm
    success_url = reverse_lazy('Products:ProductList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل وحدة منتج: ' + str(self.object)
        context['action_url'] = reverse_lazy('Products:ProductUnitUpdate', kwargs={'pk': self.kwargs['pk']})
        return context

    def get_form(self, *args, **kwargs):
        product_item = get_object_or_404(ProductUnit, id=self.kwargs['pk'])
        form = super(ProductUnitUpdate, self).get_form(*args, **kwargs)
        form.fields['unit_from'].queryset = Unit.objects.filter(deleted=False)
        form.fields['unit_name'].queryset = Unit.objects.filter(~Q(name=product_item.product.main_unit), deleted=False)
        return form


class ProductUnitDelete(UpdateView):
    model = ProductUnit
    template_name = 'Core/confirm_delete.html'
    form_class = UnitsProductFormD
    success_url = reverse_lazy('Products:ProductList')

    def form_valid(self, form):
        """
        Overridden to add the ipsum relation to the `Lorem` instance.
        """
        form.instance.deleted = 1
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف وحدة منتج: ' + str(self.object)
        context['action_url'] = reverse_lazy('Products:ProductUnitDelete', kwargs={'pk': self.kwargs['pk']})
        return context

class CustomerPricesUpdate(UpdateView):
    model = CustomerPrices
    form_class = CustomerPricesUpdateForm
    template_name = 'Core/form_template.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل الشريحة: ' + str(self.object)
        context['action_url'] = reverse_lazy('Products:CustomerPricesUpdate', kwargs={'pk': self.object.id})
        return context

    def update_product(self):
        price_menu = PricesList.objects.get(id = self.kwargs['ppk'])
        segment = Category.objects.get(name = self.object.customer_segment)        

        for x in Product.objects.filter(price_list = price_menu):
            if x.purchase_price_new_activation == False:
                for product_price in ProductPrices.objects.filter(product = x , customer_segment = segment):
                    product_price.discount = self.object.discount
                    product_price.opration = self.object.opration
                    if str(self.object.opration) == '1':
                        product_price.new_price = (x.sell_price - (self.object.discount * x.sell_price /100 ))
                    if str(self.object.opration) == '2':
                        product_price.new_price = (x.sell_price + (self.object.discount * x.sell_price /100 ))
                    product_price.save()
        return 'ok'

    def form_valid(self, form):
        self.object = form.save()
        self.update_product()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('Products:PricesListCard', kwargs={'pk': self.kwargs['ppk'] })


class CustomerPricesDelete(UpdateView):
    model = CustomerPrices
    form_class = CustomerPricesDeleteForm
    template_name = 'Core/form_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف الشريحة: ' + str(self.object)
        context['action_url'] = reverse_lazy('Products:CustomerPricesDelete', kwargs={'pk': self.object.id})
        return context
    def get_success_url(self):
        return reverse_lazy('Products:PricesListCard', kwargs={'pk': self.kwargs['ppk'] })