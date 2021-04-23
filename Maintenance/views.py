from django.shortcuts import HttpResponseRedirect, redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import *

from .forms import *


# Create your views here.
class TicketList(ListView):
    model = Ticket
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('customer_name'):
            queryset = queryset.filter(customer__name__icontains=self.request.GET.get('customer_name'))
        if self.request.GET.get('mobile'):
            queryset = queryset.filter(customer__phone__icontains=self.request.GET.get('mobile'))
        if self.request.GET.get('device_barcode'):
            queryset = queryset.filter(product__id=self.request.GET.get('device_barcode'))
        if self.request.GET.get('serial'):
            queryset = queryset.filter(sn=self.request.GET.get('serial'))
        if self.request.GET.get('employee'):
            queryset = queryset.filter(employee__id=self.request.GET.get('employee'))
        if self.request.GET.get('status'):
            if self.request.GET.get('status') != 0:
                queryset = queryset.filter(sn=self.request.GET.get('status'))
        return queryset


class TicketTrashList(ListView):
    model = Ticket
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('customer_name'):
            queryset = queryset.filter(customer__name__icontains=self.request.GET.get('customer_name'))
        if self.request.GET.get('mobile'):
            queryset = queryset.filter(customer__phone__icontains=self.request.GET.get('mobile'))
        if self.request.GET.get('device_barcode'):
            queryset = queryset.filter(product__id=self.request.GET.get('device_barcode'))
        if self.request.GET.get('serial'):
            queryset = queryset.filter(sn=self.request.GET.get('serial'))
        if self.request.GET.get('employee'):
            queryset = queryset.filter(employee__id=self.request.GET.get('employee'))
        if self.request.GET.get('status'):
            if self.request.GET.get('status') != 0:
                queryset = queryset.filter(sn=self.request.GET.get('status'))
        return queryset


class TicketCreate(CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Maintenance:TicketList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تذكرة صيانة جديدة'
        context['action_url'] = reverse_lazy('Maintenance:TicketCreate')
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.employee = self.request.user
        obj.save()
        reply = TicketReply()
        reply.employee = self.request.user
        reply.date = now()
        reply.reply = 'تم فتح التذكرة'
        reply.ticket = obj
        reply.save()
        return HttpResponseRedirect(self.get_success_url())


class TicketUpdate(UpdateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Maintenance:TicketList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل تذكرة: ' + str(self.object)
        context['action_url'] = reverse_lazy('Maintenance:TicketUpdate', kwargs={'pk': self.object.id})
        return context


class TicketDelete(UpdateView):
    model = Ticket
    form_class = TicketDeleteForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Maintenance:TicketList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف تذكرة: ' + str(self.object)
        context['action_url'] = reverse_lazy('Maintenance:TicketDelete', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class TicketDetail(DetailView):
    model = Ticket


class TransferTo(UpdateView):
    model = Ticket
    form_class = TicketTransferForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Maintenance:TicketList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تحويل إلي:'
        context['action_url'] = reverse_lazy('Maintenance:TransferTo', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

    def form_valid(self, form):
        obj = form.save()
        reply = TicketReply()
        reply.ticket = obj
        reply.employee = self.request.user
        reply.date = now()
        reply.reply = 'تم تحويل التذكرة إلي:' + str(obj.employee)
        reply.save()
        return HttpResponseRedirect(self.get_success_url())


class OutsourceTransfer(UpdateView):
    model = Ticket
    form_class = OutsourceTransferForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Maintenance:TicketList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تحويل إلي صيانة خارجية:'
        context['action_url'] = reverse_lazy('Maintenance:OutsourceTransfer', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

    def form_valid(self, form):
        obj = form.save()
        obj.outsource_status = 2
        obj.save()
        reply = TicketReply()
        reply.ticket = obj
        reply.employee = self.request.user
        reply.date = now()
        reply.reply = 'تم تحويل التذكرة إلي صيانة خارجية:' + str(obj.outsource) + '\r عن طريق شركة شحن:' + str(
            obj.shipping_company) + '\r رقم بوليصة الشحن:' + str(obj.shipping_id)
        reply.save()
        return HttpResponseRedirect(self.get_success_url())


class OutsourceReceived(UpdateView):
    model = Ticket
    form_class = OutsourceReceiveForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Maintenance:TicketList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'استلام من صيانة خارجية:'
        context['action_url'] = reverse_lazy('Maintenance:OutsourceReceived', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

    def form_valid(self, form):
        obj = form.save()
        obj.outsource_status = 3
        obj.save()
        reply = TicketReply()
        reply.ticket = obj
        reply.employee = self.request.user
        reply.date = now()
        reply.reply = 'تم استلام التذكرة من الصيانة خارجية:' + str(obj.outsource) + '\r عن طريق شركة شحن:' + str(
            obj.shipping_company2) + '\r رقم بوليصة الشحن:' + str(obj.shipping_id2)
        reply.save()
        return HttpResponseRedirect(self.get_success_url())


class Diagnosis(UpdateView):
    model = Ticket
    form_class = DiagnosisForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Maintenance:TicketList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تشخيص العطل:'
        context['action_url'] = reverse_lazy('Maintenance:CostRating', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.status = 2
        obj.save()
        reply = TicketReply()
        reply.ticket = obj
        reply.employee = self.request.user
        reply.date = now()
        reply.reply = 'تم تشخيص العطل بـ:' + str(obj.diagnosis)
        reply.save()
        return HttpResponseRedirect(self.get_success_url())


class CostRating(UpdateView):
    model = Ticket
    form_class = CostRatingForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Maintenance:TicketList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تقييم تكلفة الإصلاح:'
        context['action_url'] = reverse_lazy('Maintenance:CostRating', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.status = 3
        obj.save()
        reply = TicketReply()
        reply.ticket = obj
        reply.employee = self.request.user
        reply.date = now()
        reply.reply = 'تم تقييم تكلفة الإصلاح بـ:' + str(obj.cost)
        reply.save()
        return HttpResponseRedirect(self.get_success_url())


class CustomerReply(UpdateView):
    model = Ticket
    form_class = CustomerReplyForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Maintenance:TicketList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تم الاتصال بالعميل:'
        context['action_url'] = reverse_lazy('Maintenance:CustomerReply', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        if obj.customer_reply == 2:
            obj.status = 6
        elif obj.customer_reply == 3:
            obj.status = 4
        obj.save()
        reply = TicketReply()
        reply.ticket = obj
        reply.employee = self.request.user
        reply.date = now()
        reply.reply = 'رد العميل:' + str(obj.get_customer_reply_display())
        reply.save()
        return HttpResponseRedirect(self.get_success_url())


class TicketDone(UpdateView):
    model = Ticket
    form_class = TicketDoneForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Maintenance:TicketList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تم الانتهاء من الصيانة؟:'
        context['action_url'] = reverse_lazy('Maintenance:TicketDone', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

    def form_valid(self, form):
        obj = form.save(commit=False)
        if obj.done:
            obj.status = 7
        obj.save()
        reply = TicketReply()
        reply.ticket = obj
        reply.employee = self.request.user
        reply.date = now()
        reply.reply = 'تمت صيانة الجهاز'
        reply.save()
        return HttpResponseRedirect(self.get_success_url())


class RejectTicket(UpdateView):
    model = Ticket
    form_class = TickerRejectForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Maintenance:TicketList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'رفض صيانة جهاز:'
        context['action_url'] = reverse_lazy('Maintenance:RejectTicket', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.status = 8
        obj.save()
        reply = TicketReply()
        reply.ticket = obj
        reply.employee = self.request.user
        reply.date = now()
        reply.reply = 'لا يمكن إصلاح الجهاز السبب: ' + str(obj.reject_reason)
        reply.save()
        return HttpResponseRedirect(self.get_success_url())


class CustomerReceived(UpdateView):
    model = Ticket
    form_class = CustomerReceivedForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Maintenance:TicketList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تسليم الجهاز للعميل'
        context['action_url'] = reverse_lazy('Maintenance:CustomerReceived', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

    def form_valid(self, form):
        obj = form.save()
        reply = TicketReply()
        reply.ticket = obj
        reply.employee = self.request.user
        reply.date = now()
        reply.reply = 'تم تسليم الجهاز للعميل '
        reply.save()
        return HttpResponseRedirect(self.get_success_url())


class TicketReplyCreate(CreateView):
    model = TicketReply
    form_class = TickerReplyForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Maintenance:TicketList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'رد علي تذكرة صيانة'
        context['action_url'] = reverse_lazy('Maintenance:TicketReplyCreate', kwargs={'pk': self.kwargs.get('pk')})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

    def form_valid(self, form):
        reply = form.save(commit=False)
        reply.ticket = Ticket.objects.get(id=self.kwargs.get('pk'))
        reply.employee = self.request.user
        reply.save()
        return HttpResponseRedirect(self.get_success_url())


def get_maintenance_receipt_setting():
    try:
        setting = PrintSetting.objects.get(id=1)
    except:
        setting = PrintSetting()
        setting.save()
    return setting


def maintenance_print_setting(request):
    setting = get_maintenance_receipt_setting()
    form = MaintenancePrintSettingForm(request.POST or None, request.FILES or None, instance=setting)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        return redirect(request.POST.get('url'))
    context = {
        'title': 'إعدادات طباعة إيصالات الصيانة',
        'form': form,
    }
    return render(request, 'Core/form_template.html', context)


def print_receipt(request, pk):
    invoice = get_object_or_404(Ticket, id=pk)
    setting = get_maintenance_receipt_setting()
    context = {
        'object': invoice,
        'setting': setting,
    }
    return render(request, 'Maintenance/Print/' + str(setting.size) + '.html', context)
