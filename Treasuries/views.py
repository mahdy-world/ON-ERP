from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import *
from django.urls import reverse_lazy

from Invoices.models import TreasuryTransactions
from .models import *
from .forms import *

# Create your views here.

class TreasuryList(ListView):
    model = Treasury
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('type'):
            queryset = queryset.filter(type=self.request.GET.get('type'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        if self.request.GET.get('no'):
            queryset = queryset.filter(no__icontains=self.request.GET.get('no'))
        return queryset


class TreasuryTrashList(ListView):
    model = Treasury
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('type'):
            queryset = queryset.filter(type=self.request.GET.get('type'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        if self.request.GET.get('no'):
            queryset = queryset.filter(no__icontains=self.request.GET.get('no'))
        return queryset


class TreasuryCreate(CreateView):
    model = Treasury
    form_class = TreasuryForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Treasuries:TreasuryList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة خزينة'
        context['action_url'] = reverse_lazy('Treasuries:TreasuryCreate')
        return context

    def form_valid(self, form):
        treas = form.save()
        product_item = get_object_or_404(Treasury, id=treas.id)
        treasury_transactions = TreasuryTransactions()
        treasury_transactions.transaction = 'إضافة خزينة'
        treasury_transactions.treasury = product_item
        treasury_transactions.incoming = product_item.initial_balance
        treasury_transactions.total_incoming = product_item.initial_balance
        treasury_transactions.balance = product_item.initial_balance
        treasury_transactions.save()
        return super(TreasuryCreate, self).form_valid(form)

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class TreasuryUpdate(UpdateView):
    model = Treasury
    form_class = TreasuryForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Treasuries:TreasuryList')

    def form_valid(self, form):
        """
        Overridden to add the ipsum relation to the `Lorem` instance.
        """
        treas = form.save(commit=False)
        treasury_transactions = TreasuryTransactions.objects.filter(treasury=Treasury.objects.get(id=treas.id)).first()
        treasury_transactions.transaction = 'إضافة خزينة'
        treasury_transactions.treasury = Treasury.objects.get(id=treas.id)
        treasury_transactions.incoming = treas.initial_balance
        treasury_transactions.total_incoming = treas.initial_balance
        treasury_transactions.balance = treas.initial_balance
        treasury_transactions.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل خزينة: ' + str(self.object)
        context['action_url'] = reverse_lazy('Treasuries:TreasuryUpdate', kwargs={'pk': self.object.id})
        return context


class TreasuryDelete(UpdateView):
    model = Treasury
    form_class = TreasuryDeleteForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Treasuries:TreasuryList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف خزينة: ' + str(self.object)
        context['action_url'] = reverse_lazy('Treasuries:TreasuryDelete', kwargs={'pk': self.object.id})
        return context

class PaymentMachinesList(ListView):
    model = PaymentMachines
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(type=self.request.GET.get('name'))
        if self.request.GET.get('discount_percentage'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('discount_percentage'))
        if self.request.GET.get('transfer'):
            queryset = queryset.filter(no__icontains=self.request.GET.get('transfer'))
        return queryset

class PaymentMachinesTrashList(ListView):
    model = PaymentMachines
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(type=self.request.GET.get('name'))
        if self.request.GET.get('discount_percentage'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('discount_percentage'))
        if self.request.GET.get('transfer'):
            queryset = queryset.filter(no__icontains=self.request.GET.get('transfer'))
        return queryset

class PaymentMachinesCreate(CreateView):
    model = PaymentMachines
    form_class = PaymentMachinesForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Treasuries:PaymentMachinesList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة ماكينة دفع'
        context['action_url'] = reverse_lazy('Treasuries:PaymentMachinesCreate')
        form = self.form_class(self.request.POST or None)
        form.fields['transfer'].queryset = Treasury.objects.filter(type='2')
        context['form'] = form
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

class PaymentMachinesUpdate(UpdateView):
    model = PaymentMachines
    form_class = PaymentMachinesForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Treasuries:PaymentMachinesList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل ماكينة دفع: ' + str(self.object)
        context['action_url'] = reverse_lazy('Treasuries:PaymentMachinesUpdate', kwargs={'pk': self.object.id})
        return context


class PaymentMachinesDelete(UpdateView):
    model = PaymentMachines
    form_class = TreasuryDeleteForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Treasuries:PaymentMachinesList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف ماكينة دفع: ' + str(self.object)
        context['action_url'] = reverse_lazy('Treasuries:PaymentMachinesDelete', kwargs={'pk': self.object.id})
        return context