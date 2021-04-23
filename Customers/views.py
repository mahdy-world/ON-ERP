from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import *
from django.urls import reverse_lazy
from .models import *
from .forms import *
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from rest_framework import generics
from django.db.models import Q
from .serializers import CustomerSerializer
from Products.models import Product , ProductPrices , CustomerPrices, PricesList


# Create your views here.

#category class
class CategoryList(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Category
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        return queryset


class CategoryTrashList(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Category
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        return queryset


class CategoryCreate(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = Category
    form_class = CategoryForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Customers:CategoryList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة شريحة عملاء'
        context['action_url'] = reverse_lazy('Customers:CategoryCreate')
        return context

    def add_to_all_product(self):
        for x in Product.objects.all():
            product_price = ProductPrices()
            product_price.product = x
            product_price.customer_segment = Category.objects.get(name=self.object.name)
            product_price.price = x.sell_price
            product_price.discount = '0'
            product_price.new_price = x.sell_price
            product_price.save()
        return 'ok'
    
    def add_to_all_main_prices(self):
        for x in PricesList.objects.all():
            customer_prices = CustomerPrices()
            customer_prices.prices_list = x
            customer_prices.customer_segment = Category.objects.get(name=self.object.name)
            customer_prices.save()
        return 'ok'

    def form_valid(self, form):
        self.object = form.save()
        self.add_to_all_product()
        self.add_to_all_main_prices()
        return super().form_valid(form)

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class CategoryUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Category
    form_class = CategoryForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Customers:CategoryList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل شريحة عملاء: ' + str(self.object)
        context['action_url'] = reverse_lazy('Customers:CategoryUpdate', kwargs={'pk': self.object.id})
        return context


class CategoryDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Category
    form_class = CategoryDeleteForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Customers:CategoryList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف شريحة: ' + str(self.object)
        context['action_url'] = reverse_lazy('Customers:CategoryDelete', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


#Costumer class
class CustomerList(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Customer
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('type'):
            queryset = queryset.filter(type=self.request.GET.get('type'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        if self.request.GET.get('address'):
            queryset = queryset.filter(address__icontains=self.request.GET.get('address'))
        if self.request.GET.get('phone'):
            queryset = queryset.filter(phone__icontains=self.request.GET.get('phone'))
        if self.request.GET.get('job'):
            queryset = queryset.filter(job__icontains=self.request.GET.get('job'))
        if self.request.GET.get('category'):
            queryset = queryset.filter(category=self.request.GET.get('category'))
        if self.request.GET.get('q'):
            queryset = queryset.filter(
                Q(name__icontains=self.request.GET.get('q')) |
                Q(phone__icontains=self.request.GET.get('q')) |
                Q(facebook_account__icontains=self.request.GET.get('q'))
            )
        return queryset


class CustomerTrashList(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Customer
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('type'):
            queryset = queryset.filter(type=self.request.GET.get('type'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        if self.request.GET.get('address'):
            queryset = queryset.filter(address__icontains=self.request.GET.get('address'))
        if self.request.GET.get('phone'):
            queryset = queryset.filter(phone__icontains=self.request.GET.get('phone'))
        if self.request.GET.get('job'):
            queryset = queryset.filter(job__icontains=self.request.GET.get('job'))
        if self.request.GET.get('sales_category'):
            queryset = queryset.filter(sales_category=self.request.GET.get('sales_category'))
        if self.request.GET.get('purchases_category'):
            queryset = queryset.filter(purchases_categorygit=self.request.GET.get('purchases_category'))            
        if self.request.GET.get('q'):
            queryset = queryset.filter(
                Q(name__icontains=self.request.GET.get('q')) |
                Q(phone__icontains=self.request.GET.get('q')) |
                Q(facebook_account__icontains=self.request.GET.get('q'))
            )
        return queryset


class CustomerCreate(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = Customer
    form_class = CustomerForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Customers:CustomerList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة عميل / مورد'
        context['action_url'] = reverse_lazy('Customers:CustomerCreate')
        return context
        
    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

def customer_create(request):
    form = CustomerForm(request.POST or None)
    form2 = CustomerNotesForm(request.POST or None)
    title = 'إضافة عميل / مورد'

    if form.is_valid():
        customer = form.save()

        form2.save(commit=False)
        x = Customer.objects.get(id = customer.id)
        x.seller_feedback = form2.instance.seller_feedback
        x.accountant_notes = form2.instance.accountant_notes
        x.purchase_invoices_comments = form2.instance.purchase_invoices_comments
        x.save()
        return redirect('Customers:CustomerList')

    context = {
        'form': form,
        'title': title,
        'form2' : form2,
    }
    return render(request, 'Core/form_template.html', context)

class CustomerUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Customer
    form_class = CustomerForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Customers:CustomerList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل عميل / مورد: ' + str(self.object)
        context['action_url'] = reverse_lazy('Customers:CustomerUpdate', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class CustomerDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Customer
    form_class = CustomerDeleteForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Customers:CustomerList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف عميل / مورد: ' + str(self.object)
        context['action_url'] = reverse_lazy('Customers:CustomerDelete', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class CallReasonList(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = CallReason
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        return queryset


class CallReasonTrashList(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = CallReason
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        return queryset


class CallReasonCreate(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = CallReason
    form_class = CallReasonForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('customersCallReasonList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة سبب مكالمة'
        context['action_url'] = reverse_lazy('customersCallReasonCreate')
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class CallReasonUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = CallReason
    form_class = CallReasonForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('customersCallReasonList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل سبب المكالمة: ' + str(self.object)
        context['action_url'] = reverse_lazy('customersCallReasonUpdate', kwargs={'pk': self.object.id})
        return context


class CallReasonDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = CallReason
    form_class = CallReasonDeleteForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('customers:CallReasonList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف سبب المكالمة: ' + str(self.object)
        context['action_url'] = reverse_lazy('customers:CallReasonDelete', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class CustomerDetail(LoginRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = Customer


class CustomerInvoices(LoginRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = Customer
    template_name = 'Customers/customer_invoices.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('type'):
            context['invoices'] = self.object.invoice_set.filter(deleted=False,
                                                                 invoice_type=self.request.GET.get('type'))
        else:
            context['invoices'] = self.object.invoice_set.filter(deleted=False)
        return context


class CustomerCalls(LoginRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = Customer
    template_name = 'Customers/customer_calls.html'


class CustomerAPIList(generics.ListCreateAPIView):
    queryset = Customer.objects.filter(deleted=False)
    serializer_class = CustomerSerializer


class CustomerAPIDetail(generics.RetrieveUpdateAPIView):
    queryset = Customer.objects.filter(deleted=False)
    serializer_class = CustomerSerializer


def add_call(request, pk):
    customer = get_object_or_404(Customer, id=pk)
    form = CustomerCallForm(request.POST or None)
    if form.is_valid():
        call = form.save(commit=False)
        call.customer = customer
        call.added_by = request.user
        call.save()
        history = CustomerHistory()
        history.customer = customer
        history.added_by = request.user
        history.history_type = 2
        history.call = call
        history.save()
        return redirect(request.POST.get('url'))
    context = {
        'form': form,
        'title': 'إضافة مكالمة',
    }
    return render(request, 'Core/form_template.html', context)


class CallDetail(LoginRequiredMixin, DetailView):
    model = CustomerCall
    login_url = '/auth/login/'



#Cstomer_type class

class CustomerTypeList(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = CustomerType
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        return queryset

class CustomerTypeTrashList(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = CustomerType
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
       
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
       
        if self.request.GET.get('q'):
            queryset = queryset.filter(
                Q(name__icontains=self.request.GET.get('q')) |
                Q(phone__icontains=self.request.GET.get('q')) |
                Q(facebook_account__icontains=self.request.GET.get('q'))
            )
        return queryset        

class CustomerTypeCreate(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = CustomerType
    form_class = CustomerTypeForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Customers:CustomerTypeCreate')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة نوع عميل'
        context['action_url'] = reverse_lazy('Customers:CustomerTypeCreate')
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

class CustomerTypeUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = CustomerType
    form_class = CustomerTypeForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Customers:CustomerTypeList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل نوع العميل:' + str(self.object)
        context['action_url'] = reverse_lazy('Customers:CustomerTypeUpdate', kwargs={'pk': self.object.id})
        return context

class CustomerTypeDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = CustomerType
    form_class =  CustomerTypeDeleteForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Customers:CustomerTypeDelete')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف نوع العميل: ' + str(self.object)
        context['action_url'] = reverse_lazy('Customers:CustomerTypeDelete', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url    
