from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import *
from Invoices.models import *
from Calendar.models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q




# Create your views here.
@login_required(login_url='Auth:login')
def index(request):
    opened_invoices = Invoice.objects.filter(saved=False, deleted=False)
    return render(request, 'base.html', {'opened_invoices':opened_invoices})


class Index(LoginRequiredMixin, TemplateView):
    login_url = '/auth/login/'
    template_name = 'Core/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        context['opened_invoices'] = Invoice.objects.filter(saved=False, deleted=False)
        context['private_tasks'] = Task.objects.filter(employee=self.request.user, deleted=False, done=False, task_type=1)
        context['public_tasks'] = Task.objects.filter(deleted=False, done=False, task_type=2)

       
        
        return context





class ChangeLog(TemplateView):
    template_name = 'Core/change_log.html'


def fix(request):
    for x in Invoice.objects.filter(invoice_type__in=[1, 2, 3, 4]):
        x.calculate_profit()
    return redirect('Core:index')


def update(request):
    invoices = Invoice.objects.all()
    from_branch = [1, 2, 3, 6, 7]
    to_branch = [4, 5]
    to_treasury = [1, 2, 3, 6, 7]
    from_treasury = [4, 5]
    for x in invoices.filter(invoice_type__in=from_branch):
        if x.creator:
            x.from_branch = x.creator.default_branch
            x.save()
    for x in invoices.filter(invoice_type__in=to_branch):
        if x.creator:
            x.to_branch = x.creator.default_branch
            x.save()
    for x in invoices.filter(invoice_type__in=from_treasury):
        if x.creator:
            x.from_treasury = x.creator.default_treasury
            x.save()
    for x in invoices.filter(invoice_type__in=to_treasury):
        if x.creator:
            x.to_treasury = x.creator.default_treasury
            x.save()
    context = {
        'title': 'تم التحديث بنجاح',
    }
    return render(request, 'base.html', context)


def chat_index(request):
    return render(request, 'empty_base.html') 

