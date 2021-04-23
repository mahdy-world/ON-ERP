from django.shortcuts import render
from django.views.generic import *
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin


# Create your views here.
class TechnicianList(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    title = 'عرض الفنيين'
    model = Technician
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        return queryset


class TechnicianTrashList(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Technician
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        return queryset


class TechnicianCreate(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = Technician
    form_class = TechnicianForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Technicians:TechnicianList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة فني'
        context['action_url'] = reverse_lazy('Technicians:TechnicianCreate')
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class TechnicianUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Technician
    form_class = TechnicianForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Technicians:TechnicianList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل بيانات فني: ' + str(self.object)
        context['action_url'] = reverse_lazy('Technicians:TechnicianUpdate', kwargs={'pk': self.object.id})
        return context


class TechnicianDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Technician
    form_class = TechnicianDeleteForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Technicians:TechnicianList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف فني: ' + str(self.object)
        context['action_url'] = reverse_lazy('Technicians:TechnicianDelete', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url
