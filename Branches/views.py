from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import *
from django.urls import reverse_lazy
from .models import *
from .forms import *


# Create your views here.

#Branch Class 
class BranchList(ListView):
    model = Branch
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
        return queryset


class BranchTrashList(ListView):
    model = Branch
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
        return queryset


class BranchCreate(CreateView):
    model = Branch
    form_class = BranchForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Branches:BranchList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة فرع'
        context['action_url'] = reverse_lazy('Branches:BranchCreate')
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class BranchUpdate(UpdateView):
    model = Branch
    form_class = BranchForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Branches:BranchList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل فرع: ' + str(self.object)
        context['action_url'] = reverse_lazy('Branches:BranchUpdate', kwargs={'pk': self.object.id})
        return context


class BranchDelete(UpdateView):
    model = Branch
    form_class = BranchDeleteForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Branches:BranchList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف فرع: ' + str(self.object)
        context['action_url'] = reverse_lazy('Branches:BranchDelete', kwargs={'pk': self.object.id})
        return context


#Warehouse Class 

class WarehouseList(ListView):
    model = Warehouse
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
        return queryset


class WarehouseCreate(CreateView):
    model = Warehouse
    form_class = WarehouseForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Branches:WarehouseList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة مخزن'
        context['action_url'] = reverse_lazy('Branches:WarehouseCreate')
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class WarehouseUpdate(UpdateView):
    model = Warehouse
    form_class = WarehouseForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Branches:WarehouseList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل  المخازن: ' + str(self.object)
        context['action_url'] = reverse_lazy('Branches:WarehouseUpdate', kwargs={'pk': self.object.id})
        return context


class WarehouseDelete(UpdateView):
    model = Warehouse
    form_class = WarehouseDeleteForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Branches:WarehouseList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف المخزن: ' + str(self.object)
        context['action_url'] = reverse_lazy('Branches:WarehouseDelete', kwargs={'pk': self.object.id})
        return context


class WarehouseTrashList(ListView):
    model = Warehouse
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))

        if self.request.GET.get('branch'):
            queryset = queryset.filter(branch__icontains=slef.request.Get.get('branch'))           
        return queryset


def branch_warehouse_create(request, pk):
    context = {
            'title': 'تعديل مخازن الفرع'
        }
    branch = get_object_or_404(Branch, id=pk)
    try:
        obj = BranchWarehouses.objects.get(branch__id=pk)
        form = BranchWarehousesForm(request.POST or None, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.branch = branch
            obj.save()
            return redirect('Branches:BranchList')
        context.update({'form': form})
        return render(request, 'Core/form_template.html', context)
    except:
        form = BranchWarehousesForm(request.POST or None)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.branch = branch
            obj.save()
            return redirect('Branches:BranchList')
        context.update({'form': form})
        return render(request, 'Core/form_template.html', context)

        


    