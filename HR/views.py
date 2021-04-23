from django.shortcuts import render, get_object_or_404
from django.views.generic import *
from django.urls import reverse_lazy
from .models import *
from .forms import *
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin


# Create your views here.
class EmployeeDetail(LoginRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = Employee


class EmployeeList(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Employee
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.all()
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        if self.request.GET.get('phone'):
            queryset = queryset.filter(phone__icontains=self.request.GET.get('phone'))
        if self.request.GET.get('address'):
            queryset = queryset.filter(address__icontains=self.request.GET.get('address'))
        if self.request.GET.get('job_title'):
            queryset = queryset.filter(job_title__name__icontains=self.request.GET.get('job_title'))
        return queryset


class EmployeeCreate(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = Employee
    form_class = EmployeeForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('HR:EmployeeList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة موظف'
        context['action_url'] = reverse_lazy('HR:EmployeeCreate')
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class EmployeeUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Employee
    form_class = EmployeeForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('HR:EmployeeList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل موظف: ' + str(self.object)
        context['action_url'] = reverse_lazy('HR:EmployeeUpdate', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class EmployeeDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Employee
    form_class = EmployeeDeleteForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('HR:EmployeeList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف موظف: ' + str(self.object)
        context['action_url'] = reverse_lazy('HR:EmployeeDelete', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class UploadFile(LoginRequiredMixin, CreateView):
    model = EmployeeFile
    form_class = EmployeeFileForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('HR:EmployeeList')

    def form_valid(self, form):
        """
        Overridden to add the ipsum relation to the `Lorem` instance.
        """
        employee = get_object_or_404(Employee, id=self.kwargs['pk'])
        form.instance.employee = employee
        form.instance.uploaded_by = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'رفع ملف موظف: ' + str(get_object_or_404(Employee, id=self.kwargs['pk']))
        print(self.kwargs['pk'])
        context['action_url'] = reverse_lazy('HR:UploadFile', kwargs={'pk': self.kwargs['pk']})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class ViewFile(LoginRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = EmployeeFile


class UserCreate(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = User
    form_class = UserForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة حساب لموظف: ' + str(get_object_or_404(Employee, id=self.kwargs['pk']))
        print(self.kwargs['pk'])
        context['action_url'] = reverse_lazy('HR:UploadFile', kwargs={'pk': self.kwargs['pk']})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url
