from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views.generic import *
from django.urls import reverse_lazy
from .forms import *
from Customers.forms import CustomerForm
from .models import MagedInvoice as Invoice, MagedInvoiceItems as InvoiceItem
from django.db.models import Q
# Create your views here.
def get_invoice_base_setting():
    try:
        setting = InvoiceBaseSetting.objects.get(id=1)
    except:
        setting = InvoiceBaseSetting()
        setting.save()
    return setting


def get_invoices(request, invoice_type=None):
    if request.user.is_superuser:
        invoices = Invoice.objects.all()
        if invoice_type:
            invoices = invoices.filter(invoice_type=int(invoice_type))
    else:
        invoices = Invoice.objects.filter(employee=request.user, deleted=False)
        if invoice_type:
            invoices = invoices.filter(invoice_type=int(invoice_type))
    return invoices


def make_invoice(request, type):
    setting = get_invoice_base_setting()
    invoice = Invoice(invoice_type=type)
    if setting.default_customer_in_sales:
        if invoice.invoice_type == 1:
            invoice.customer = setting.default_customer_in_sales
    invoice.branch = request.user.default_branch
    invoice.treasury = request.user.default_treasury
    invoice.main_warehouse = BranchWarehouses.objects.get(branch=invoice.branch).main_warehouse
    invoice.sub_warehouse = BranchWarehouses.objects.get(branch=invoice.branch).sub_warehouse
    invoice.employee = request.user
    invoice.save()
    return redirect('InvoicesMaged:show_invoice', invoice.id)


def show_invoice(request, pk):
    message = ''
    warning = []
    setting = get_invoice_base_setting()
    invoice = get_object_or_404(Invoice, id=pk)
    out_stock_invoices = [1, 2, 3, 6, 15]
    in_stock_invoices = [4, 5, 16]
    #in_treasury_invoices = [1, 2, 3, 6, 12]
    #out_treasury_invoices = [4, 5, 11]
    invoices = get_invoices(request, invoice.invoice_type).order_by('id')
    prev_invoice = invoices.filter(id__lt=invoice.id).last()
    next_invoice = invoices.filter(id__gt=invoice.id).first()
    opened_invoices = Invoice.objects.filter(saved=False, invoice_type=invoice.invoice_type, deleted=False)
    saved_invoices = Invoice.objects.filter(saved=True, paid=False, invoice_type=invoice.invoice_type, deleted=False)
    paid_invoices = Invoice.objects.filter(saved=True, paid=True, out_of_warehouse=False, invoice_type=invoice.invoice_type, deleted=False)
    out_invoices = Invoice.objects.filter(saved=True, paid=True, out_of_warehouse=True, invoice_type=invoice.invoice_type, deleted=False)
    categories = Category.objects.filter(deleted=False)
    products = Product.objects.all()
    form = InvoiceItemForm(request.POST or None)
    form.fields['item'].queryset = Product.objects.filter(deleted=False)
    context = {
        'invoice': invoice,
        'opened_invoices': opened_invoices,
        'saved_invoices': saved_invoices,
        'paid_invoices': paid_invoices,
        'out_invoices': out_invoices,
        'categories': categories,
        'products': products,
        'form': form,
        'prev_invoice': prev_invoice,
        'next_invoice': next_invoice,
        'out_stock_invoices': out_stock_invoices,
        'in_stock_invoices': in_stock_invoices,
        #'in_treasury_invoices': in_treasury_invoices,
        #'out_treasury_invoices': out_treasury_invoices,

    }
    invoice.calculate()
    if form.is_valid():
        item = form.save(commit=False)
        if invoice.branch:
            item_stock = item.item.branch_stock(invoice.branch.id)
        else:
            item_stock = item.item.current_stock()
        if invoice.invoice_type in [1, 2, 6]:
            if not setting.sell_without_stock:
                if not item_stock - item.quantity >= 0:
                    message = 'عفواً لا يوجد رصيد كافٍ. الرصيد المتاح: ' + str(item_stock)
                    messages.add_message(request, messages.ERROR, extra_tags='danger', message=message)
                    return render(request, 'Invoices/OneByOne/invoice_detail_m.html', context)
            if setting.alert_on_critical_storage:
                if not item_stock - item.quantity > item.item.critical_stock:
                    message = 'المنتج: ' + item.item.name + ".وصل للرصيد الحرج."
                    messages.add_message(request, messages.WARNING, message)
            if setting.alert_on_min_cost_price:
                if item.unit_price <= item.item.cost_price:
                    warning = 'تنبيه: سعر البيع أقل من سعر التكلفة'
                    if request.user.has_perm('Invoices.access_purchase_invoice_menu'):
                        message = ' سعر التكلفة: ' + str(item.item.cost_price)
                    messages.add_message(request, messages.WARNING, message)
            if setting.alert_on_min_purchase_price:
                if item.unit_price <= item.item.purchase_price:
                    message = 'تنبيه: سعر البيع أقل من سعر الشراء'
                    if request.user.has_perm('Invoices.access_purchase_invoice_menu'):
                        message = ' سعر الشراء: ' + str(item.item.purchase_price)
                    messages.add_message(request, messages.WARNING, message)

        if invoice.invoice_type == 5:
            if setting.update_cost_profit_on_purchase:
                item.item.cost_price = item.unit_price
                item.item.save()

        item.invoice = invoice
        if invoice.invoice_type in [1, 2, 3, 4, 7]:
            if item.unit_price == 0.0:
                item.unit_price = item.item.sell_price
        elif invoice.invoice_type in [5, 6]:
            if item.unit_price == 0.0:
                item.unit_price = item.item.cost_price

        item.total_price = item.unit_price * item.quantity
        item.after_discount = item.total_price - item.discount
        item.save()
        item.calculate_profit()
        invoice.calculate()
        # return render(request, 'Invoices/OneByOne/invoice_detail.html', context)
        return redirect('InvoicesMaged:show_invoice', invoice.id)
    return render(request, 'Invoices/OneByOne/invoice_detail_m.html', context)


def save_invoice(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    setting = get_invoice_base_setting()
    if invoice.saved:
        return render(request, 'empty_base.html', context={'alert': 'هذه الفاتورة محفوظة بالفعل'})
    if not invoice.invoice_type in [15, 16, 17]:
        if not invoice.customer:
            return render(request, 'empty_base.html', context={'alert': 'يجب اختيار العميل/المورد قبل الحفظ'})
    if invoice.invoice_type in [1, 2, 4, 5, 6]:
        if not invoice.treasury:
            return render(request, 'empty_base.html', context={'alert': 'يجب اختيار الخزينة قبل الحفظ'})
        if not invoice.branch:
            return render(request, 'empty_base.html', context={'alert': 'يجب اختيار الفرع قبل الحفظ'})

    invoice.calculate()
    invoice.employee = request.user
    action_url = reverse_lazy('InvoicesMaged:save_invoice', kwargs={'pk': invoice.id})
    invoice.save()
    if invoice.invoice_type in [1, 2, 3, 6]:
        form = SalesInvoiceForm(request.POST or None, instance=invoice)
    elif invoice.invoice_type in [4, 5]:
        form = PurchaseInvoiceForm(request.POST or None, instance=invoice)
    elif invoice.invoice_type in [15, 16]:
        form = PlusMinusForm(request.POST or None, instance=invoice)
    elif invoice.invoice_type == 7:
        form = QuotationForm(request.POST or None, instance=invoice)
    elif invoice.invoice_type == 17:
        form = StockTransferSaveForm(request.POST or None, instance=invoice)

    if form.is_valid():
        obj = form.save(commit=False)
        obj.saved = 1
        obj.save()
        invoice.save_invoice()
        # if setting.update_cost_profit_on_purchase:
        #     invoice.update_cost_profit()
        return redirect('InvoicesMaged:show_invoice', invoice.id)
    context = {
        'form': form,
        'action_url': action_url,
    }
    return render(request, 'Core/form_template.html', context)


def pay_invoice(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    setting = get_invoice_base_setting()
    if invoice.paid:
        return render(request, 'empty_base.html', context={'alert': 'هذه الفاتورة مدفوعة بالفعل'})
    if not invoice.invoice_type in [15, 16, 17]:
        if not invoice.customer:
            return render(request, 'empty_base.html', context={'alert': 'يجب اختيار العميل/المورد قبل الحفظ'})
    if invoice.invoice_type in [1, 2, 4, 5, 6]:
        if not invoice.treasury:
            return render(request, 'empty_base.html', context={'alert': 'يجب اختيار الخزينة قبل الحفظ'})
        if not invoice.branch:
            return render(request, 'empty_base.html', context={'alert': 'يجب اختيار الفرع قبل الحفظ'})

    invoice.calculate()
    invoice.employee = request.user
    action_url = reverse_lazy('InvoicesMaged:pay_invoice', kwargs={'pk': invoice.id})
    invoice.save()
    if invoice.invoice_type in [1, 2, 3, 6]:
        form = SalesPaidInvoiceForm(request.POST or None, instance=invoice)
    elif invoice.invoice_type in [4, 5]:
        form = PurchasePaidInvoiceForm(request.POST or None, instance=invoice)
    elif invoice.invoice_type in [15, 16]:
        form = PlusMinusForm(request.POST or None, instance=invoice)
    elif invoice.invoice_type == 7:
        form = QuotationForm(request.POST or None, instance=invoice)
    elif invoice.invoice_type == 17:
        form = StockTransferSaveForm(request.POST or None, instance=invoice)

    if form.is_valid():
        obj = form.save(commit=False)
        if invoice.invoice_type in [4, 5]:
            form.instance.customer_debit = obj.after_discount - obj.outgoing
        elif invoice.invoice_type in [1, 2, 3, 6]:
            form.instance.customer_credit = obj.after_discount - obj.incoming
        obj.paid = 1
        obj.save()
        # invoice.save_invoice()
        # if setting.update_cost_profit_on_purchase:
        #     invoice.update_cost_profit()
        return redirect('InvoicesMaged:show_invoice', invoice.id)
    context = {
        'form': form,
        'action_url': action_url,
    }
    return render(request, 'Core/form_template.html', context)


def out_invoice(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    if invoice.out_of_warehouse:
        return render(request, 'empty_base.html', context={'alert': 'هذه الفاتورة تمت تسويتها بالفعل'})
    action_url = reverse_lazy('InvoicesMaged:out_invoice', kwargs={'pk': invoice.id})
    form = OutInvoiceForm(request.POST or None, instance=invoice)
    if form.is_valid():
        form.save()
        invoice.out_of_warehouse = 1
        invoice.employee = request.user
        invoice.save(update_fields=['out_of_warehouse', 'employee'])
        return redirect('InvoicesMaged:show_invoice', invoice.id)
    context = {
        'form': form,
        'action_url': action_url,
    }
    return render(request, 'Core/form_template.html', context)


def unsave_invoice(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    invoice.calculate()
    invoice.employee = request.user
    invoice.save()
    action_url = reverse_lazy('InvoicesMaged:unsave_invoice', kwargs={'pk': invoice.id})
    form = InvoiceUnSaveForm(request.POST or None, instance=invoice)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        return redirect('InvoicesMaged:show_invoice', invoice.id)
    context = {
        'form': form,
        'action_url': action_url,
    }
    return render(request, 'Core/form_template.html', context)


def delete_invoice(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    invoice_type = invoice.invoice_type
    title = "حذف " + invoice.__str__()
    action_url = reverse_lazy('InvoicesMaged:delete_invoice', kwargs={'pk': invoice.id})
    form = InvoiceDeleteForm(request.POST or None, instance=invoice)
    if form.is_valid():
        form.save()
        return redirect('InvoicesMaged:show_opened_invoices', invoice_type)
    context = {
        'title': title,
        'form': form,
        'action_url': action_url,
    }
    return render(request, 'Core/form_template.html', context)


def show_opened_invoices(request, type):
    opened_invoices = Invoice.objects.filter(saved=False, invoice_type=type, deleted=False)
    context = {
        'opened_invoices': opened_invoices,
        'type': type,
    }
    return render(request, 'Invoices/OneByOne/opened_invoices_m.html', context)


def delete_invoice_item(request, pk):
    item = get_object_or_404(InvoiceItem, id=pk)
    invoice = item.invoice
    item.delete()
    invoice.calculate()
    return redirect('InvoicesMaged:show_invoice', invoice.id)


def edit_invoice_item_price(request, pk):
    setting = get_invoice_base_setting()
    item = get_object_or_404(InvoiceItem, id=pk)
    invoice = item.invoice
    if invoice.branch:
        item_stock = item.item.branch_stock(invoice.branch.id)
    else:
        item_stock = item.item.current_stock()
    form = InvoiceItemPriceUpdateForm(request.POST or None, instance=item)
    title = 'تعديل سعر ' + item.item.name
    action_url = reverse_lazy('InvoicesMaged:edit_invoice_item_price', kwargs={'pk': item.id})
    if form.is_valid():
        item = form.save(commit=False)
        if invoice.invoice_type in [1, 2, 6]:
            if setting.alert_on_min_cost_price:
                if item.unit_price <= item.item.cost_price:
                    message = 'تنبيه: سعر البيع أقل من سعر التكلفة'
                    if request.user.has_perm('Invoices.access_purchase_invoice_menu'):
                        message += ' سعر التكلفة: ' + str(item.item.cost_price)
                    messages.add_message(request, messages.WARNING, message)
            if setting.alert_on_min_purchase_price:
                if item.unit_price <= item.item.purchase_price:
                    message = 'تنبيه: سعر البيع أقل من سعر الشراء'
                    if request.user.has_perm('Invoices.access_purchase_invoice_menu'):
                        message += ' سعر الشراء: ' + str(item.item.purchase_price)
                    messages.add_message(request, messages.WARNING, message)

        item.calculate()
        return redirect('InvoicesMaged:show_invoice', item.invoice.id)
    context = {
        'title': title,
        'form': form,
        'action_url': action_url,
    }
    return render(request, 'Core/form_template.html', context)

def calculate_main_units(inv_item_id):
    invoice_item = InvoiceItem.objects.get(id=inv_item_id)

    units = {}
    units_1 = []
    u = 1.0
    y = 1.0
    product_units_1 = ProductUnit.objects.filter(Q(unit_name=invoice_item.item.main_unit) | Q(unit_from=invoice_item.item.main_unit), product=invoice_item.item, deleted=0)
    product_units_2 = ProductUnit.objects.filter(~Q(unit_name=invoice_item.item.main_unit), ~Q(unit_from=invoice_item.item.main_unit), product=invoice_item.item, deleted=0)
    product_units_all = ProductUnit.objects.filter(product=invoice_item.item, deleted=0)

    if invoice_item.item.main_unit != None:
        for unit1 in product_units_1:
            result = float(unit1.unit_quantity)
            units[unit1.id] = result
            units_1.append(result)

        for i in units_1:
            u *= i

        for x in product_units_all:
            y *= x.unit_quantity

        for unit2 in product_units_2:
            if product_units_2.filter(unit_name=unit2.unit_from).exists()==False:
                if unit2.unit_from != None:
                    result = float(unit2.unit_quantity) * u
                    units[unit2.id] = result
                else:
                    result = y
                    units[unit2.id] = result
            else:
                un = product_units_2.get(unit_name=unit2.unit_from)
                uu = units[un.id]
                result = float(unit2.unit_quantity) * uu
                units[unit2.id] = result

    if invoice_item.unit_name != invoice_item.item.main_unit:
        prod_units = ProductUnit.objects.get(product=invoice_item.item, unit_name=invoice_item.unit_name)
        invoice_item.main_unit_quantity = units[prod_units.id] * invoice_item.quantity
        invoice_item.main_unit_main_warehouse = units[prod_units.id] * invoice_item.main_warehouse
        invoice_item.main_unit_sub_warehouse = units[prod_units.id] * invoice_item.sub_warehouse
    else:
        invoice_item.main_unit_quantity = invoice_item.quantity
        invoice_item.main_unit_main_warehouse = invoice_item.main_warehouse
        invoice_item.main_unit_sub_warehouse = invoice_item.sub_warehouse

    return 1000



def edit_invoice_item_quantity(request, pk):
    item = get_object_or_404(InvoiceItem, id=pk)
    invoice = item.invoice
    setting = get_invoice_base_setting()
    if invoice.branch:
        item_stock = item.item.branch_stock(invoice.branch.id)
    else:
        item_stock = item.item.current_stock()

    if invoice.main_warehouse:
        main_store_stock = item.item.main_store_stock(invoice.main_warehouse.id)
    else:
        main_store_stock = item.item.current_stock()

    if invoice.sub_warehouse:
        sub_store_stock = item.item.sub_store_stock(invoice.sub_warehouse.id)
    else:
        sub_store_stock = item.item.current_stock()

    form = InvoiceItemQuantityUpdateForm(request.POST or None, instance=item)
    title = 'تعديل كمية ' + item.item.name
    action_url = reverse_lazy('InvoicesMaged:edit_invoice_item_quantity', kwargs={'pk': item.id})
    if form.is_valid():
        item = form.save(commit=False)
        invoice_item = get_object_or_404(InvoiceItem, id=item.id)
        current_stock = InvoiceItem.objects.filter(invoice=invoice_item.invoice.id).aggregate(
            total_all=Sum('main_unit_quantity'), total_main=Sum('main_unit_main_warehouse'), total_sub=Sum('main_unit_sub_warehouse'))
        i = calculate_main_units(item.id)

        print(i)

        if invoice.invoice_type in [1, 2, 6]:
            if not setting.sell_without_stock:
                if invoice_item.main_unit_quantity > item_stock - float(current_stock['total_all']):
                    message = 'عفواً لا يوجد رصيد كافٍ. الرصيد المتاح: ' + str(item_stock - float(current_stock['total_all'])) + ' ' + str(invoice_item.item.main_unit.name)
                    messages.add_message(request, messages.ERROR, extra_tags='danger', message=message)
                    return redirect('InvoicesMaged:show_invoice', invoice.id)
                elif invoice_item.main_unit_main_warehouse > main_store_stock - float(current_stock['total_main']):
                    message = 'عفواً لاتوجد كمية كافية داخل المخزن الرئيسي. الكمية المتاحة: ' + str(main_store_stock - float(current_stock['total_main'])) + ' ' + str(invoice_item.item.main_unit.name)
                    messages.add_message(request, messages.ERROR, extra_tags='danger', message=message)
                    return redirect('InvoicesMaged:show_invoice', invoice.id)
                elif invoice_item.main_unit_sub_warehouse > sub_store_stock - float(current_stock['total_sub']):
                    message = 'عفواً لاتوجد كمية كافية داخل المخزن الفرعي. الكمية المتاحة: ' + str(sub_store_stock - float(current_stock['total_sub'])) + ' ' + str(invoice_item.item.main_unit.name)
                    messages.add_message(request, messages.ERROR, extra_tags='danger', message=message)
                    return redirect('InvoicesMaged:show_invoice', invoice.id)

            if setting.alert_on_critical_storage:
                if not item_stock - invoice_item.main_unit_quantity > item.item.critical_stock:
                    message = 'المنتج: ' + item.item.name + ".وصل للرصيد الحرج."
                    messages.add_message(request, messages.WARNING, message)


        # if invoice.invoice_type in [1, 2, 6]:
        #     if not setting.sell_without_stock:
        #         if not item_stock - item.quantity >= 0:
        #             message = 'عفواً لا يوجد رصيد كافٍ. الرصيد المتاح: ' + str(item_stock)
        #             messages.add_message(request, messages.ERROR, extra_tags='danger', message=message)
        #             return redirect('InvoicesMaged:show_invoice', item.invoice.id)
        #     if setting.alert_on_critical_storage:
        #         if not item_stock - item.quantity > item.item.critical_stock:
        #             message = 'المنتج: ' + item.item.name + ".وصل للرصيد الحرج."
        #             messages.add_message(request, messages.WARNING, message)

        form.instance.main_warehouse = item.quantity
        form.instance.sub_warehouse = 0.0
        form.save()
        item.calculate()
        return redirect('InvoicesMaged:show_invoice', item.invoice.id)
    context = {
        'title': title,
        'form': form,
        'action_url': action_url,
    }
    return render(request, 'Core/form_template.html', context)


def edit_invoice_item_main_warehouse(request, pk):
    item = get_object_or_404(InvoiceItem, id=pk)
    invoice = item.invoice
    setting = get_invoice_base_setting()
    if invoice.branch:
        item_stock = item.item.branch_stock(invoice.branch.id)
    else:
        item_stock = item.item.current_stock()
    form = InvoiceItemMainWarehouseUpdateForm(request.POST or None, instance=item)
    title = 'تعديل كمية المخزن الرئيسي ' + item.item.name
    action_url = reverse_lazy('InvoicesMaged:edit_invoice_item_main_warehouse', kwargs={'pk': item.id})
    if form.is_valid():
        item = form.save(commit=False)
        # if item.main_warehouse > item.quantity - item.sub_warehouse:
        #     message = 'عفواً الكمية المتبقية للتخزين أقل من تلك الكمية, الكمية المتبقية: ' + str(item.quantity - item.sub_warehouse)
        #     messages.add_message(request, messages.ERROR, extra_tags='danger', message=message)
        #     return redirect('InvoicesMaged:show_invoice', item.invoice.id)
        form.instance.sub_warehouse = item.quantity - item.main_warehouse
        form.save()
        item.calculate()
        return redirect('InvoicesMaged:show_invoice', item.invoice.id)
    context = {
        'title': title,
        'form': form,
        'action_url': action_url,
    }
    return render(request, 'Core/form_template.html', context)


def edit_invoice_item_sub_warehouse(request, pk):
    item = get_object_or_404(InvoiceItem, id=pk)
    invoice = item.invoice
    setting = get_invoice_base_setting()
    if invoice.branch:
        item_stock = item.item.branch_stock(invoice.branch.id)
    else:
        item_stock = item.item.current_stock()
    form = InvoiceItemSubWarehouseUpdateForm(request.POST or None, instance=item)
    title = 'تعديل كمية المخزن الفرعي ' + item.item.name
    action_url = reverse_lazy('InvoicesMaged:edit_invoice_item_sub_warehouse', kwargs={'pk': item.id})
    if form.is_valid():
        item = form.save(commit=False)
        # if item.sub_warehouse > item.quantity - item.main_warehouse:
        #     message = 'عفواً الكمية المتبقية للتخزين أقل من تلك الكمية, الكمية المتبقية: ' + str(item.quantity - item.main_warehouse)
        #     messages.add_message(request, messages.ERROR, extra_tags='danger', message=message)
        #     return redirect('InvoicesMaged:show_invoice', item.invoice.id)
        form.instance.main_warehouse = item.quantity - item.sub_warehouse
        form.save()
        item.calculate()
        return redirect('InvoicesMaged:show_invoice', item.invoice.id)
    context = {
        'title': title,
        'form': form,
        'action_url': action_url,
    }
    return render(request, 'Core/form_template.html', context)



def edit_invoice_date(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    form = InvoiceDateForm(request.POST or None, instance=invoice)
    title = 'تعديل تاريخ فاتورة ' + invoice.__str__()
    action_url = reverse_lazy('InvoicesMaged:edit_invoice_date', kwargs={'pk': invoice.id})
    if form.is_valid():
        form.save()
        invoice.calculate()
        return redirect('InvoicesMaged:show_invoice', invoice.id)
    context = {
        'title': title,
        'form': form,
        'action_url': action_url,
    }
    return render(request, 'Core/form_template.html', context)


def edit_invoice_item_discount(request, pk):
    item = get_object_or_404(InvoiceItem, id=pk)
    form = InvoiceItemDiscountUpdateForm(request.POST or None, instance=item)
    title = 'تعديل خصم ' + item.item.name
    action_url = reverse_lazy('InvoicesMaged:edit_invoice_item_discount', kwargs={'pk': item.id})
    if form.is_valid():
        form.save()
        item.calculate()
        return redirect('InvoicesMaged:show_invoice', item.invoice.id)
    context = {
        'title': title,
        'form': form,
        'action_url': action_url,
    }
    return render(request, 'Core/form_template.html', context)


def edit_invoice_discount(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    title = 'تعديل خصم فاتورة'
    action_url = reverse_lazy('InvoicesMaged:edit_invoice_discount', kwargs={'pk': invoice.id})
    form = InvoiceDiscountUpdateForm(request.POST or None, instance=invoice)
    if form.is_valid():
        invoice = form.save(commit=False)
        invoice.save()
        invoice.calculate_after_discount()
        return redirect('InvoicesMaged:show_invoice', invoice.id)
    context = {
        'title': title,
        'action_url': action_url,
        'form': form,
    }
    return render(request, 'Core/form_template.html', context)


def edit_invoice_customer(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    title = 'العميل / مورد'
    action_url = reverse_lazy('InvoicesMaged:edit_invoice_customer', kwargs={'pk': invoice.id})
    form = InvoiceCustomerForm(request.POST or None, instance=invoice)
    form.fields['customer'].queryset = Customer.objects.filter(deleted=False)
    if form.is_valid():
        invoice = form.save(commit=False)
        invoice.save()
        history = CustomerHistory()
        if invoice.invoice_type == 1:
            history.history_type = 4
        if invoice.invoice_type == 7:
            history.history_type = 3
        if invoice.invoice_type == 4:
            history.history_type = 5
        if invoice.invoice_type == 5:
            history.history_type = 6
        if invoice.invoice_type == 6:
            history.history_type = 7
        history.customer = invoice.customer
        history.invoice_id = invoice.id
        history.added_by = request.user
        history.save()
        return redirect('InvoicesMaged:show_invoice', invoice.id)
    context = {
        'title': title,
        'action_url': action_url,
        'form': form,
    }
    return render(request, 'Core/form_template.html', context)


def edit_invoice_branch(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    title = 'الفرع'
    action_url = reverse_lazy('InvoicesMaged:edit_invoice_branch', kwargs={'pk': invoice.id})
    if invoice.invoice_type in [1, 2, 3, 6, 7, 15]:
        form = InvoiceFromBranchForm(request.POST or None, instance=invoice)
    if invoice.invoice_type in [4, 5, 16]:
        form = InvoiceToBranchForm(request.POST or None, instance=invoice)
    if invoice.invoice_type == 17:
        form = BranchTransferForm(request.POST or None, instance=invoice)
    if not request.user.is_superuser:
        form.fields['branch'].queryset = request.user.allowed_branches.filter(deleted=False)
    else:
        form.fields['branch'].queryset = Branch.objects.filter(deleted=False)

    if form.is_valid():
        invoice = form.save(commit=False)
        invoice.main_warehouse = BranchWarehouses.objects.get(branch=invoice.branch).main_warehouse
        invoice.sub_warehouse = BranchWarehouses.objects.get(branch=invoice.branch).sub_warehouse
        invoice.save()
        return redirect('InvoicesMaged:show_invoice', invoice.id)
    context = {
        'title': title,
        'action_url': action_url,
        'form': form,
    }
    return render(request, 'Core/form_template.html', context)


def edit_invoice_treasury(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    title = 'الخزينة'
    action_url = reverse_lazy('InvoicesMaged:edit_invoice_treasury', kwargs={'pk': invoice.id})
    if invoice.invoice_type in [1, 2, 3, 6]:
        form = InvoiceToTreasuryForm(request.POST or None, instance=invoice)
    if invoice.invoice_type in [4, 5]:
        form = InvoiceFromTreasuryForm(request.POST or None, instance=invoice)
    if not request.user.is_superuser:
        form.fields['treasury'].queryset = request.user.allowed_treasuries.filter(branch=invoice.branch, deleted=False)
    else:
        form.fields['treasury'].queryset = Treasury.objects.filter(branch=invoice.branch, deleted=False)
    if form.is_valid():
        invoice = form.save(commit=False)
        invoice.save()
        return redirect('InvoicesMaged:show_invoice', invoice.id)
    context = {
        'title': title,
        'action_url': action_url,
        'form': form,
    }
    return render(request, 'Core/form_template.html', context)


def get_unit_price(request, invoice_id):
    product = get_object_or_404(Product, id=request.GET.get('product_id'))
    invoice = get_object_or_404(Invoice, id=invoice_id)
    cust = invoice.customer
    customer = get_object_or_404(Customer, id=cust.id)
    cat = customer.category
    category = None
    if cat:
        category = get_object_or_404(Category, id=cat.id)

    product_price = ProductPrices.objects.filter(inactive=False, deleted=False, product=product, customer_segment=category)
    if invoice.invoice_type in [1, 2, 3, 4, 7]:
        if product_price:
            product_price = ProductPrices.objects.get(inactive=False, deleted=False, product=product, customer_segment=category)
            return HttpResponse(product_price.price)
        else:
            return HttpResponse(product.sell_price)
    if invoice.invoice_type in [5, 6]:
        if product_price:
            product_price = ProductPrices.objects.get(inactive=False, deleted=False, product=product, customer_segment=category)
            return HttpResponse(product_price.price)
        else:
            return HttpResponse(product.sell_price)


def get_product_units(request):
    if request.is_ajax():
        product = get_object_or_404(Product, id=request.GET.get('product_id'))
        produc_units = ProductUnit.objects.filter(product=product)
        # form = InvoiceItemForm(request.POST or None)
        # form.fields['unit_name'].queryset = produc_units
        return render(request, 'Invoices/OneByOne/product_units_filter.html', {'produc_units': produc_units, 'product':product})


def expense_invoice(request):
    title = 'إذن صرف نقدية'
    form = ExpenseInvoiceForm(request.POST or None)
    if not request.user.is_superuser:
        form.fields['treasury'].querset = request.user.allowed_treasuries.all()
        if not request.user.has_perm('Invoices.edit_invoice_date'):
            form.fields['date'].disabled = True
    form.initial['treasury'] = request.user.default_treasury
    action_url = reverse_lazy('InvoicesMaged:expense_invoice')
    if form.is_valid():
        obj = form.save(commit=False)
        obj.invoice_type = 11
        obj.creator = request.user
        obj.saved = True
        obj.save()
        url = request.POST.get('url')
        return redirect(url)
    context = {
        'title': title,
        'form': form,
        'action_url': action_url,
    }
    return render(request, 'Core/form_template.html', context)


def edit_fast_invoice(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    title = 'تعديل ' + str(invoice)
    if invoice.invoice_type == 11:
        form = ExpenseInvoiceForm(request.POST or None, instance=invoice)
    if invoice.invoice_type == 12:
        form = IncomeInvoiceForm(request.POST or None, instance=invoice)
    elif invoice.invoice_type == 13:
        form = CapitalIncomeForm(request.POST or None, instance=invoice)
    elif invoice.invoice_type == 14:
        form = CapitalOutcomeForm(request.POST or None, instance=invoice)
    elif invoice.invoice_type == 19:
        form = TreasuryTransferForm(request.POST or None, instance=invoice)
    if not request.user.is_superuser:
        form.fields['treasury'].querset = User.allowed_treasuries.all()
        if not request.user.has_perm('Invoices.edit_invoice_date'):
            form.fields['date'].disabled = True
    action_url = reverse_lazy('InvoicesMaged:edit_fast_invoice', kwargs={'pk': invoice.id})
    if form.is_valid():
        obj = form.save(commit=False)
        if invoice.invoice_type == 19:
            obj.treasury = form.cleaned_data['treasury']
        obj.saved = True
        obj.save()
        url = request.POST.get('url')
        return redirect(url)
    context = {
        'title': title,
        'form': form,
        'action_url': action_url,
    }
    return render(request, 'Core/form_template.html', context)


def income_invoice(request):
    title = 'إذن قبض نقدية'
    form = IncomeInvoiceForm(request.POST or None)
    if not request.user.is_superuser:
        form.fields['treasury'].querset = request.user.allowed_treasuries.all()
        if not request.user.has_perm('Invoices.edit_invoice_date'):
            form.fields['date'].disabled = True
    form.initial['treasury'] = request.user.default_treasury
    action_url = reverse_lazy('InvoicesMaged:income_invoice')
    if form.is_valid():
        obj = form.save(commit=False)
        obj.invoice_type = 12
        obj.creator = request.user
        obj.saved = True
        obj.save()
        url = request.POST.get('url')
        return redirect(url)
    context = {
        'title': title,
        'form': form,
        'action_url': action_url,
    }
    return render(request, 'Core/form_template.html', context)


def get_last_invoice(request, type):
    invoices = get_invoices(request, int(type)).order_by('id')
    last_invoice = invoices.last()
    if last_invoice:
        return redirect('InvoicesMaged:show_invoice', last_invoice.id)
    else:
        return redirect('InvoicesMaged:show_opened_invoices', int(type))


def search_invoice(request):
    id = request.GET.get('invoice_id')
    invoice_f = Invoice.objects.filter(id=id)
    if invoice_f:
        invoice = get_object_or_404(Invoice, id=id)
        return redirect('InvoicesMaged:show_invoice', invoice.id)
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def get_invoice_setting():
    try:
        setting = InvoiceSetting.objects.get(id=1)
    except:
        setting = InvoiceSetting()
        setting.save()
    return setting


def invoice_base_setting(request):
    setting = get_invoice_base_setting()
    form = BaseSettingForm(request.POST or None, request.FILES or None, instance=setting)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        return redirect(request.POST.get('url'))
    context = {
        'title': 'إعدادات الفواتير',
        'form': form,
    }
    return render(request, 'Core/form_template.html', context)


def invoice_setting(request):
    setting = get_invoice_setting()
    form = SettingForm(request.POST or None, request.FILES or None, instance=setting)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        return redirect(request.POST.get('url'))
    context = {
        'title': 'إعدادات طباعة الفواتير',
        'form': form,
    }
    return render(request, 'Core/form_template.html', context)


def print_invoice(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    setting = get_invoice_setting()
    context = {
        'invoice': invoice,
        'setting': setting,
    }
    return render(request, 'Invoices/Print/' + str(setting.size) + '_m.html', context)


# def customer_income(request):
#     title = 'إذن قبض سداد'
#     form = CustomerIncomeForm(request.POST or None)
#     if request.GET.get('customer'):
#         customer = get_object_or_404(Customer, id=request.GET.get('customer'))
#         form.initial['customer'] = customer
#     if not request.user.is_superuser:
#         form.fields['treasury'].querset = request.user.allowed_treasuries.all()
#     form.initial['treasury'] = request.user.default_treasury
#     action_url = reverse_lazy('Invoices:income_invoice')
#     if form.is_valid():
#         obj = form.save(commit=False)
#         obj.invoice_type = 21
#         obj.creator = request.user
#         obj.saved = True
#         obj.save()
#         obj.calculate()
#         url = request.POST.get('url')
#         return redirect(url)
#     context = {
#         'title': title,
#         'form': form,
#         'action_url': action_url,
#     }
#     return render(request, 'Core/form_template.html', context)


# def customer_outcome(request):
#     title = 'إذن صرف سداد'
#     form = CustomerOutcomeForm(request.POST or None)
#     if request.GET.get('customer'):
#         customer = get_object_or_404(Customer, id=request.GET.get('customer'))
#         form.initial['customer'] = customer
#     if not request.user.is_superuser:
#         form.fields['treasury'].querset = request.user.allowed_treasuries.all()
#     form.initial['treasury'] = request.user.default_treasury
#     action_url = reverse_lazy('Invoices:income_invoice')
#     if form.is_valid():
#         obj = form.save(commit=False)
#         obj.invoice_type = 22
#         obj.creator = request.user
#         obj.saved = True
#         obj.save()
#         obj.calculate()
#         url = request.POST.get('url')
#         return redirect(url)
#     context = {
#         'title': title,
#         'form': form,
#         'action_url': action_url,
#     }
#     return render(request, 'Core/form_template.html', context)


def capital_plus(request):
    title = 'إضافة لرأس المال'
    form = CapitalIncomeForm(request.POST or None)
    if not request.user.is_superuser:
        form.fields['treasury'].querset = request.user.allowed_treasuries.all()
        if not request.user.has_perm('Invoices.edit_invoice_date'):
            form.fields['date'].disabled = True
    form.initial['treasury'] = request.user.default_treasury
    action_url = reverse_lazy('InvoicesMaged:income_invoice')
    if form.is_valid():
        obj = form.save(commit=False)
        obj.invoice_type = 13
        obj.creator = request.user
        obj.saved = True
        obj.save()
        url = request.POST.get('url')
        return redirect(url)
    context = {
        'title': title,
        'form': form,
        'action_url': action_url,
    }
    return render(request, 'Core/form_template.html', context)


def capital_minus(request):
    title = 'سحب من رأس المال'
    form = CapitalOutcomeForm(request.POST or None)
    if not request.user.is_superuser:
        form.fields['treasury'].querset = request.user.allowed_treasuries.all()
        if not request.user.has_perm('Invoices.edit_invoice_date'):
            form.fields['date'].disabled = True
    form.initial['treasury'] = request.user.default_treasury
    action_url = reverse_lazy('InvoicesMaged:income_invoice')
    if form.is_valid():
        obj = form.save(commit=False)
        obj.invoice_type = 14
        obj.creator = request.user
        obj.saved = True
        obj.save()
        url = request.POST.get('url')
        return redirect(url)
    context = {
        'title': title,
        'form': form,
        'action_url': action_url,
    }
    return render(request, 'Core/form_template.html', context)


def super_delete(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    invoice_type = invoice.invoice_type
    invoices = get_invoices(request, invoice.invoice_type).order_by('id')
    prev_invoice = invoices.filter(id__lt=invoice.id).last()
    next_invoice = invoices.filter(id__gt=invoice.id).first()
    invoice.delete()
    if prev_invoice:
        return redirect(reverse_lazy('InvoicesMaged:show_invoice', kwargs={'pk': prev_invoice.id}))
    elif next_invoice:
        return redirect(reverse_lazy('InvoicesMaged:show_invoice', kwargs={'pk': prev_invoice.id}))
    else:
        return redirect(reverse_lazy('InvoicesMaged:get_last_invoice', kwargs={'type': invoice_type}))


def treasury_transfer(request):
    title = 'تحويل خزينة'
    form = TreasuryTransferForm(request.POST or None)
    if form.is_valid():
        invoice = form.save(commit=False)
        invoice.invoice_type = 19
        invoice.treasury = form.cleaned_data['treasury']
        invoice.saved = True
        invoice.creator = request.user
        invoice.save()
        url = request.POST.get('url')
        return redirect(url)
    context = {
        'title': title,
        'form': form,
    }
    return render(request, 'Core/form_template.html', context)


# class SpendCategoryList(ListView):
#     model = SpendCategory
#     paginate_by = 100
#
#     def get_queryset(self):
#         queryset = self.model.objects.filter(deleted=False)
#         if self.request.GET.get('id'):
#             queryset = queryset.filter(id=self.request.GET.get('id'))
#         if self.request.GET.get('name'):
#             queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
#         return queryset


# class SpendCategoryTrashList(ListView):
#     model = SpendCategory
#     paginate_by = 100
#
#     def get_queryset(self):
#         queryset = self.model.objects.filter(deleted=True)
#         if self.request.GET.get('id'):
#             queryset = queryset.filter(id=self.request.GET.get('id'))
#         if self.request.GET.get('name'):
#             queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
#         return queryset


# class SpendCategoryCreate(CreateView):
#     model = SpendCategory
#     form_class = SpendCategoryForm
#     template_name = 'Core/form_template.html'
#     success_url = reverse_lazy('Invoices:SpendCategoryList')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'إضافة تصنيف مصروفات'
#         context['action_url'] = reverse_lazy('Invoices:SpendCategoryCreate')
#         return context
#
#     def get_success_url(self):
#         if self.request.POST.get('url'):
#             return self.request.POST.get('url')
#         else:
#             return self.success_url


# class SpendCategoryUpdate(UpdateView):
#     model = SpendCategory
#     form_class = SpendCategoryForm
#     template_name = 'Core/form_template.html'
#     success_url = reverse_lazy('Invoices:SpendCategoryList')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'تعديل تصنيف مصروفات: ' + str(self.object)
#         context['action_url'] = reverse_lazy('Invoices:SpendCategoryUpdate', kwargs={'pk': self.object.id})
#         return context


# class SpendCategoryDelete(UpdateView):
#     model = SpendCategory
#     form_class = SpendCategoryDeleteForm
#     template_name = 'Core/form_template.html'
#     success_url = reverse_lazy('Invoices:SpendCategoryList')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'حذف تصنيف مصروفات: ' + str(self.object)
#         context['action_url'] = reverse_lazy('Invoices:SpendCategoryDelete', kwargs={'pk': self.object.id})
#         return context


def add_customer_to_invoice(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    form = CustomerForm(request.POST or None)
    if form.is_valid():
        customer = form.save(commit=False)
        customer.save()
        invoice.customer = customer
        invoice.save()
        return redirect('InvoicesMaged:show_invoice', pk)
    context = {
        'title': 'إضافة عميل / مورد',
        'form': form,
    }
    return render(request, 'Core/form_template.html', context)

#####################################################

def add_product_to_invoice(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    form = InvoiceItemForm(request.POST or None)

    item = form.save(commit=False)
    inv = invoice
    setting = get_invoice_base_setting()
    if inv.branch:
        item_stock = item.item.branch_stock(inv.branch.id)
    else:
        item_stock = item.item.current_stock()

    if inv.main_warehouse:
        main_store_stock = item.item.main_store_stock(inv.main_warehouse.id)
    else:
        main_store_stock = item.item.current_stock()

    if inv.sub_warehouse:
        sub_store_stock = item.item.sub_store_stock(inv.sub_warehouse.id)
    else:
        sub_store_stock = item.item.current_stock()

    if form.is_valid():
        # item = form.save(commit=False)
        # if invoice.invoice_type in [1, 2, 6]:
        #     if not setting.sell_without_stock:
        #         if not item_stock - item.quantity >= 0:
        #             message = 'عفواً لا يوجد رصيد كافٍ. الرصيد المتاح: ' + str(item_stock)
        #             messages.add_message(request, messages.ERROR, extra_tags='danger', message=message)
        #             return redirect('InvoicesMaged:show_invoice', invoice.id)
        #     if setting.alert_on_critical_storage:
        #         if not item_stock - item.quantity > item.item.critical_stock:
        #             message = 'المنتج: ' + item.item.name + ".وصل للرصيد الحرج."
        #             messages.add_message(request, messages.WARNING, message)

        prod = form.save(commit=False)
        form.instance.invoice = invoice
        # form.instance.main_unit_quantity = 0.0
        prod.save()
        invoice_item = get_object_or_404(InvoiceItem, id=prod.id)
        current_stock = InvoiceItem.objects.filter(invoice=invoice_item.invoice.id).aggregate(
            total_all=Sum('main_unit_quantity'), total_main=Sum('main_unit_main_warehouse'), total_sub=Sum('main_unit_sub_warehouse'))

        invoice_item.calculate_main_units()
        if invoice.invoice_type in [1, 2, 6]:
            if not setting.sell_without_stock:
                if invoice_item.main_unit_quantity > item_stock - float(current_stock['total_all']):
                    invoice_item.delete()
                    message = 'عفواً لا يوجد رصيد كافٍ. الرصيد المتاح: ' + str(item_stock - float(current_stock['total_all'])) + ' ' + str(invoice_item.item.main_unit.name)
                    messages.add_message(request, messages.ERROR, extra_tags='danger', message=message)
                    return redirect('InvoicesMaged:show_invoice', invoice.id)
                elif invoice_item.main_unit_main_warehouse > main_store_stock - float(current_stock['total_main']):
                    invoice_item.delete()
                    message = 'عفواً لاتوجد كمية كافية داخل المخزن الرئيسي. الكمية المتاحة: ' + str(main_store_stock - float(current_stock['total_main'])) + ' ' + str(invoice_item.item.main_unit.name)
                    messages.add_message(request, messages.ERROR, extra_tags='danger', message=message)
                    return redirect('InvoicesMaged:show_invoice', invoice.id)
                elif invoice_item.main_unit_sub_warehouse > sub_store_stock - float(current_stock['total_sub']):
                    invoice_item.delete()
                    message = 'عفواً لاتوجد كمية كافية داخل المخزن الفرعي. الكمية المتاحة: ' + str(sub_store_stock - float(current_stock['total_sub'])) + ' ' + str(invoice_item.item.main_unit.name)
                    messages.add_message(request, messages.ERROR, extra_tags='danger', message=message)
                    return redirect('InvoicesMaged:show_invoice', invoice.id)

            if setting.alert_on_critical_storage:
                if not item_stock - invoice_item.main_unit_quantity > prod.item.critical_stock:
                    message = 'المنتج: ' + prod.item.name + ".وصل للرصيد الحرج."
                    messages.add_message(request, messages.WARNING, message)

    return redirect('InvoicesMaged:show_invoice', invoice.id)


def get_unit_all_price(request, invoice_id):
    myarr = request.GET.get('myarr').split(',')

    product = get_object_or_404(Product, id=int(myarr[0]))
    unit = get_object_or_404(Unit, id=int(myarr[1]))

    product_main_unit = product.main_unit

    invoice = get_object_or_404(Invoice, id=invoice_id)
    cust = invoice.customer
    customer = get_object_or_404(Customer, id=cust.id)
    cat = customer.category
    category = None
    if cat:
        category = get_object_or_404(Category, id=cat.id)

    prod_price = ProductPrices.objects.filter(inactive=False, deleted=False, product=product, customer_segment=category)
    if prod_price:
        product_price = ProductPrices.objects.get(inactive=False, deleted=False, product=product, customer_segment=category).price
    else:
        product_price = product.sell_price

    res = 0.0
    if unit == product_main_unit:
        res = float(product_price)
    else:
        if ProductUnit.objects.filter(product=product, unit_name=unit):
            product_unit = ProductUnit.objects.get(product=product, unit_name=unit)
            if product_main_unit == product_unit.unit_from:
                res = float(product_unit.unit_quantity) * float(product_price)
            else:
                units = {}
                units_1 = []
                u = 1.0
                y = 1.0
                product_units_1 = ProductUnit.objects.filter(Q(unit_name=product.main_unit) | Q(unit_from=product.main_unit), product=product, deleted=0)
                product_units_2 = ProductUnit.objects.filter(~Q(unit_name=product.main_unit), ~Q(unit_from=product.main_unit), product=product, deleted=0)
                product_units_all = ProductUnit.objects.filter(product=product, deleted=0)

                if product.main_unit != None:
                    for unit1 in product_units_1:
                        result = float(unit1.unit_quantity)
                        units[unit1.unit_name.id] = result
                        units_1.append(result)

                    for i in units_1:
                        u *= i


                    for x in product_units_all:
                        y *= x.unit_quantity


                    for unit2 in product_units_2:
                        if product_units_2.filter(unit_name=unit2.unit_from).exists()==False:
                            if unit2.unit_from != None:
                                result = float(unit2.unit_quantity) * u
                                units[unit2.unit_name.id] = result
                            else:
                                result = y * float(product_price)
                                units[unit2.unit_name.id] = result
                        else:
                            un = product_units_2.get(unit_name=unit2.unit_from)
                            uu = units[un.unit_name.id]
                            result = float(unit2.unit_quantity) * uu
                            units[unit2.unit_name.id] = result

                res = float(units[int(myarr[1])]) * float(product_price)

    return HttpResponse(res)
