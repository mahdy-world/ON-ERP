from django.shortcuts import render, redirect
from django.views.generic import *
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from .forms import *
from django.urls import reverse_lazy


# Create your views here.
class TaskCreate(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = Task
    form_class = TaskForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Calendar:TaskCreate')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة موعد/مهام'
        context['action_url'] = reverse_lazy('Calendar:TaskCreate')
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

    def get_initial(self):
        created_date = now()
        return {
            'created_date': created_date,
        }

    def form_valid(self, form):
        object = form.save(commit=False)
        object.assigned_by = self.request.user
        object.save()
        reply = TaskRespond()
        reply.done_by = self.request.user
        reply.created_date = now()
        reply.task = object
        reply.comment = '''
        تم إنشاء الموعد
        المنشئ: {0}
        محول إلي: {1}
        تاريخ: {2}
        المحتوي: {3}
        النوع: {4}
        متعلق بـ: {5}
        '''.format(self.request.user, object.employee, object.date.isoformat(), object.comment, object.get_task_type_display(), object.related_to)
        reply.save()
        return redirect(self.request.POST.get('url'))


class TaskList(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Task
    paginate_by = 100
    template_name = 'Calendar/calendar_list.html'
    ordering = '-date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TaskForm
        context['action_url'] = reverse_lazy('Calendar:TaskCreate')
        return context

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = self.model.objects.filter(deleted=False)
        else:
            queryset = self.request.user.own_tasks.filter(deleted=False)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('task_type') in ['1', '2']:
            queryset = queryset.filter(task_type=self.request.GET.get('task_type'))
        if self.request.GET.get('comment'):
            queryset = queryset.filter(comment__icontains=self.request.GET.get('comment'))
        if self.request.GET.get('from_date'):
            queryset = queryset.filter(date__gte=self.request.GET.get('from_date'))
        if self.request.GET.get('to_date'):
            queryset = queryset.filter(date__lte=self.request.GET.get('to_date'))
        if self.request.GET.get('related_to'):
            queryset = queryset.filter(related_to__id=self.request.GET.get('related_to'))
        if self.request.GET.get('employee'):
            queryset = queryset.filter(employee__id=self.request.GET.get('employee'))
        if self.request.GET.get('done') in ['True', 'False']:
            queryset = queryset.filter(done=self.request.GET.get('done'))
        return queryset


class TaskTrashList(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Task
    paginate_by = 100
    template_name = 'Calendar/calendar_list.html'
    ordering = '-date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TaskForm
        context['action_url'] = reverse_lazy('Calendar:TaskCreate')
        return context

   


class TaskView(LoginRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = Task
    template_name = 'Calendar/calendar_view.html'


class TaskUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Task
    form_class = TaskForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Calendar:TaskList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل موعد/مهام'
        context['action_url'] = reverse_lazy('Calendar:TaskUpdate', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

    def form_valid(self, form):
        object = form.save(commit=False)
        object.save()
        reply = TaskRespond()
        reply.done_by = self.request.user
        reply.created_date = now()
        reply.task = self.object
        reply.comment = '''
        تم تعديل الموعد إلي
        محول إلي: {0}
        تاريخ: {1}
        المحتوي: {2}
        النوع: {3}
        متعلق بـ: {4}
        '''.format(object.employee, object.date.isoformat(), object.comment, object.get_task_type_display(), object.related_to)
        reply.save()
        return redirect(self.request.POST.get('url'))


class TaskDone(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Task
    form_class = TaskDoneForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Calendar:TaskList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إنهاء موعد'
        context['action_url'] = reverse_lazy('Calendar:TaskDone', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

    def form_valid(self, form):
        object = form.save(commit=False)
        object.save()
        reply = TaskRespond()
        reply.done_by = self.request.user
        reply.created_date = now()
        reply.task = self.object
        reply.comment = '''
        تم إكمال الموعد
        '''
        reply.save()
        return redirect(self.request.POST.get('url'))


class TaskDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Task
    form_class = TaskDeleteForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Calendar:TaskList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف موعد/مهام'
        context['action_url'] = reverse_lazy('Calendar:TaskDelete', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

    def form_valid(self, form):
        object = form.save(commit=False)
        object.save()
        reply = TaskRespond()
        reply.done_by = self.request.user
        reply.created_date = now()
        reply.task = self.object
        reply.comment = '''
        تم حذف الموعد
        '''
        reply.save()
        return redirect(self.request.POST.get('url'))


class TaskTransfer(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Task
    form_class = TaskTransferForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Calendar:TaskList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تحويل موعد/مهام'
        context['action_url'] = reverse_lazy('Calendar:TaskTransfer', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

    def form_valid(self, form):
        object = form.save(commit=False)
        object.save()
        reply = TaskRespond()
        reply.done_by = self.request.user
        reply.created_date = now()
        reply.task = self.object
        reply.comment = '''
        تم تحويل الموعد إلي: 
        ''' + object.employee.__str__()
        reply.save()
        return redirect(self.request.POST.get('url'))
