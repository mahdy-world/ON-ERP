from django.shortcuts import render, get_object_or_404, redirect
from Auth.models import User ,LastSeen
from django.views.generic import *
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from .forms import *
from django.urls import reverse_lazy


class TaskCreate(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = Task
    form_class = TaskForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Tasks:TaskCreate')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة موعد/مهام'
        context['action_url'] = reverse_lazy('Tasks:TaskCreate')
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

    def get_form(self, *args, **kwargs):
        
        form = super(TaskCreate, self).get_form(*args, **kwargs)
        form.fields['created_by'].initial = self.request.user
        return form
            

    def form_valid(self,form):
        object = form.save(commit=False)
        object.created_by = self.request.user
        object.save()
        reply = TaskComment()
        reply.done_by = self.request.user
        reply.created_by =now()
        reply.task = object
        reply.comment = '''
        تم انشاءمهمة
        المنشئ: {0}
        التاريخ: {1}
        الموظف: {2}
        متعلق بي : {3}
        '''.format(self.request.user ,  object.due_date , object.assigned_to_user ,object.message)
        reply.save()
        return redirect(self.request.POST.get('url'))            


class TaskList(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Task
    paginate_by = 100
    template_name = 'Tasks/task_list.html'
    ordering = '-date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TaskForm
        context['action_url'] = reverse_lazy('Tasks:TaskCreate')
        return context

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = self.model.objects.filter(deleted=False)
        else:
            queryset = self.request.user.own_tasks.filter(deleted=False)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('title'):
            queryset = queryset.filter(title__icontains=self.request.GET.get('title'))
        if self.request.GET.get('created_date'):
                queryset = queryset.filter(created_date__gte=self.request.GET.get('created_date'))
        if self.request.GET.get('due_date'):
            queryset = queryset.filter(due_date__lte=self.request.GET.get('due_date'))
        if self.request.GET.get('created_by'):
            queryset = queryset.filter(created_by__id = self.request.GET.get('created_by'))  
        if self.request.GET.get('message'):
            queryset = queryset.filter(message__id = self.request.Get.get('message'))   
        if self.request.GET.get('assigned_to_user'):
            queryset = queryset.filter(assigned_to_user__id =self.request.GET.get('assigned_to_user'))
        if self.request.GET.get('assigned_to_group'):
            queryset = queryset.filter(assigned_to_group__id = self.request.GET.get('assigned_to_group'))           
        return queryset

        



class TaskView(LoginRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = Task
    template_name = 'Tasks/task_view.html'


class TaskUpdate(LoginRequiredMixin,UpdateView):
    login_url = '/auth/login/'
    model = Task
    form_class = TaskForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Tasks:TaskList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل مهام'
        context['action_url'] = reverse_lazy('Tasks:TaskUpdate', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

    def form_valid(self,form):
        object = form.save(commit=False)
        object.created_by = self.request.user
        object.save()
        reply = TaskComment()
        reply.done_by = self.request.user
        reply.created_by =now()
        reply.task = self.object
        reply.comment = '''
        تم تعديل المهمة 
        المنشئ: {0}
        التاريخ: {1}
        الموظف: {2}
        متعلق بي : {3}
        

        
        '''.format(self.request.user ,  object.due_date , object.assigned_to_user ,object.message)
        reply.save()
        return redirect(self.request.POST.get('url'))            


class TaskDone(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Task
    form_class = TaskDoneForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Tasks:TaskList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إنهاء المهمة'
        context['action_url'] = reverse_lazy('Tasks:TaskDone', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

    def form_valid(self, form):
        object = form.save(commit=False)
        object.save()
        reply = TaskComment()
        reply.done_by = self.request.user
        reply.created_date = now()
        reply.task = self.object
        reply.comment = '''
        تم إكمال المهمة
        '''
        reply.save()
        return redirect(self.request.POST.get('url'))                 

    


class TaskDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Task
    form_class = TaskDeleteForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Tasks:TaskList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف المهمة'
        context['action_url'] = reverse_lazy('Tasks:TaskDelete', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

    def form_valid(self, form):
        object = form.save(commit=False)
        object.save()
        reply = TaskComment()
        reply.done_by = self.request.user
        reply.created_date = now()
        reply.task = self.object
        reply.comment = '''
        تم حذف المهمة
        '''
        reply.save()
        return redirect(self.request.POST.get('url'))

class TaskTrashListMain(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Task
    paginate_by = 100
    template_name = 'Tasks/task_list.html'
    ordering = '-date'

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TaskForm
        context['action_url'] = reverse_lazy('TaskTrashListMain:TaskCreate')
        return context

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True)
        return queryset


class TaskListDone(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Task
    paginate_by = 100
    template_name = 'Tasks/task_list.html'
    ordering = '-date'

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TaskForm
        context['action_url'] = reverse_lazy('Tasks:TaskCreate')
        return context

    def get_queryset(self):
        queryset = self.model.objects.filter(completed=True)
        return queryset

class TaskTransfer(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Task
    form_class = TaskTransferForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Tasks:TaskList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تحويل موعد/مهام'
        context['action_url'] = reverse_lazy('Tasks:TaskTransfer', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

    def form_valid(self, form):
        object = form.save(commit=False)
        object.save()
        reply =TaskComment()
        reply.done_by = self.request.user
        reply.created_date = now()
        reply.task = self.object
        reply.comment = '''
        تم تحويل المهمة إلي: 
        ''' + object.assigned_to_user.__str__()
        reply.save()
        return redirect(self.request.POST.get('url'))
        



    
    
    
