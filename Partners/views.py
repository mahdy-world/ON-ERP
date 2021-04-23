from django.shortcuts import render
from django.views.generic import *
from django.urls import reverse_lazy
from .models import *
from .forms import *
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin


# Create your views here.
class PartnerList(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Partner
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        if self.request.GET.get('phone'):
            queryset = queryset.filter(phone__icontains=self.request.GET.get('phone'))
        return queryset


class PartnerTrashList(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Partner
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        if self.request.GET.get('phone'):
            queryset = queryset.filter(phone__icontains=self.request.GET.get('phone'))
        return queryset


class PartnerCreate(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = Partner
    form_class = PartnerForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Partner:PartnerList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة شريك'
        context['action_url'] = reverse_lazy('Partners:PartnerCreate')
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class PartnerUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Partner
    form_class = PartnerForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Partners:PartnerList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل شريك: ' + str(self.object)
        context['action_url'] = reverse_lazy('Partners:PartnerUpdate', kwargs={'pk': self.object.id})
        return context


class PartnerDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Partner
    form_class = PartnerDeleteForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Partners:PartnerList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف شريك: ' + str(self.object)
        context['action_url'] = reverse_lazy('Partners:PartnerDelete', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url
