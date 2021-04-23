from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views.generic import *
from django.urls import reverse_lazy
from .forms import *
from Customers.forms import CustomerForm


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
        invoices = Invoice.objects.filter(creator=request.user, deleted=False)
        if invoice_type:
            invoices = invoices.filter(invoice_type=int(invoice_type))
    return invoices


def make_invoice(request, type):
    setting = get_invoice_base_setting()
    invoice = Invoice(invoice_type=type)
    if setting.default_customer_in_sales:
        if invoice.invoice_type == 1:
            invoice.customer = setting.default_customer_in_sales
    if type in [1, 2, 3, 6, 7, 15]:
        invoice.from_branch = request.user.default_branch
        invoice.to_treasury = request.user.default_treasury
        if BranchWarehouses.objects.filter(branch=invoice.from_branch):
            invoice.main_warehouse = BranchWarehouses.objects.get(branch=invoice.from_branch).main_warehouse
            invoice.sub_warehouse = BranchWarehouses.objects.get(branch=invoice.from_branch).sub_warehouse
    if type in [4, 5, 16]:
        invoice.to_branch = request.user.default_branch
        invoice.from_treasury = request.user.default_treasury
        if BranchWarehouses.objects.filter(branch=invoice.to_branch):
            invoice.main_warehouse = BranchWarehouses.objects.get(branch=invoice.to_branch).main_warehouse
            invoice.sub_warehouse = BranchWarehouses.objects.get(branch=invoice.to_branch).sub_warehouse

    invoice.creator = request.user
    invoice.save()
    return redirect('Invoices:show_invoice', invoice.id)


def show_invoice(request, pk):
    message = ''
    warning = []
    setting = get_invoice_base_setting()
    invoice = get_object_or_404(Invoice, id=pk)
    out_stock_invoices = [1, 2, 3, 6, 15]
    in_stock_invoices = [4, 5, 16]
    in_treasury_invoices = [1, 2, 3, 6, 12]
    out_treasury_invoices = [4, 5, 11]
    invoices = get_invoices(request, invoice.invoice_type).order_by('id')
    prev_invoice = invoices.filter(id__lt=invoice.id).last()
    next_invoice = invoices.filter(id__gt=invoice.id).first()
    deleted_invoices = Invoice.objects.filter(invoice_type=invoice.invoice_type, deleted=True)
    opened_invoices = Invoice.objects.filter(saved=False, invoice_type=invoice.invoice_type, deleted=False)
    saved_invoices = Invoice.objects.filter(saved=True, paid=False, out_of_warehouse=False, invoice_type=invoice.invoice_type, deleted=False)
    paid_invoices = Invoice.objects.filter(saved=True, paid=True, out_of_warehouse=False,
                                           invoice_type=invoice.invoice_type, deleted=False)
    out_invoices = Invoice.objects.filter(saved=True, paid=True, out_of_warehouse=True,
                                          invoice_type=invoice.invoice_type, deleted=False)
    out_invoices2 = Invoice.objects.filter(saved=True, out_of_warehouse=True,
                                          invoice_type=17, deleted=False)
    categories = Category.objects.filter(deleted=False)
    products = Product.objects.all()
    form = InvoiceItemForm(request.POST or None)
    if invoice.invoice_type in [1, 2, 3, 6, 7, 15]:
        items_arr = []
        item_transactions = WarehouseTransactions.objects.filter(Q(warehouse=invoice.main_warehouse) | Q(warehouse=invoice.sub_warehouse), item__deleted=False, balance__gt=0).values('item_id').distinct()
        for trans in item_transactions:
            items_arr.append(trans['item_id'])
            form.fields['item'].queryset = Product.objects.filter(id__in=items_arr, deleted=False)
    if invoice.invoice_type in [4, 5, 16]:
        form.fields['item'].queryset = Product.objects.filter(deleted=False)
    # warehouses = None
    # if invoice.from_branch and BranchWarehouses.objects.filter(branch=invoice.from_branch):
    #     warehouses = BranchWarehouses.objects.get(branch=invoice.from_branch)
    # elif invoice.to_branch and BranchWarehouses.objects.filter(branch=invoice.to_branch):
    #     warehouses = BranchWarehouses.objects.get(branch=invoice.to_branch)
    context = {
        'invoice': invoice,
        'deleted_invoices': deleted_invoices,
        'opened_invoices': opened_invoices,
        'saved_invoices': saved_invoices,
        'paid_invoices': paid_invoices,
        'out_invoices': out_invoices,
        'out_invoices2': out_invoices2,
        'categories': categories,
        'products': products,
        'form': form,
        'prev_invoice': prev_invoice,
        'next_invoice': next_invoice,
        'out_stock_invoices': out_stock_invoices,
        'in_stock_invoices': in_stock_invoices,
        'in_treasury_invoices': in_treasury_invoices,
        'out_treasury_invoices': out_treasury_invoices,
        # 'warehouses': warehouses,
        'buy_invoices': [4, 5],
        'sell_invoices': [1, 6],
        'display_invoices': [7],
        'move_stock_invoices': [17],
        'deficit_settlement_invoices': [15],
        'increase_settlement_invoices': [16],
        'display_all_prods': [1, 2, 3, 6, 7, 15],

    }
    if form.is_valid():
        item = form.save(commit=False)
        if invoice.from_branch or invoice.to_branch:
            if invoice.from_branch:
                item_stock = item.item.branch_stock(invoice.from_branch.id)
            if invoice.to_branch:
                item_stock = item.item.branch_stock(invoice.to_branch.id)
        else:
            item_stock = item.item.current_stock()
        if invoice.invoice_type in [1, 2, 6]:
            if not setting.sell_without_stock:
                if not item_stock - item.quantity >= 0:
                    message = 'عفواً لا يوجد رصيد كافٍ. الرصيد المتاح: ' + str(item_stock)
                    messages.add_message(request, messages.ERROR, extra_tags='danger', message=message)
                    return render(request, 'Invoices/OneByOne/invoice_detail.html', context)
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
        return redirect('Invoices:show_invoice', invoice.id)
    return render(request, 'Invoices/OneByOne/invoice_detail.html', context)


def save_invoice(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    invoice_items = InvoiceItem.objects.filter(invoice=invoice)
    setting = get_invoice_base_setting()
    if not invoice_items:
        return render(request, 'empty_base.html', context={'alert': 'يجب اضافة منتجات الى الفاتورة قبل الحفظ'})
    if invoice.saved:
        return render(request, 'empty_base.html', context={'alert': 'هذه الفاتورة محفوظة بالفعل'})
    if not invoice.invoice_type in [15, 16, 17]:
        if not invoice.customer:
            return render(request, 'empty_base.html', context={'alert': 'يجب اختيار العميل/المورد قبل الحفظ'})
    if invoice.invoice_type in [17]:
        if not invoice.from_warehouse or not invoice.to_warehouse:
            return render(request, 'empty_base.html', context={'alert': 'يجب اختيار المخازن قبل الحفظ'})
    if invoice.invoice_type in [1, 2, 4, 5, 6]:
        if not invoice.from_treasury and not invoice.to_treasury:
            return render(request, 'empty_base.html', context={'alert': 'يجب اختيار الخزينة قبل الحفظ'})
        if not invoice.from_branch and not invoice.to_branch:
            return render(request, 'empty_base.html', context={'alert': 'يجب اختيار الفرع قبل الحفظ'})

    # invoice.calculate()
    invoice.creator = request.user
    action_url = reverse_lazy('Invoices:save_invoice', kwargs={'pk': invoice.id})
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
        obj.saved = True
        obj.save()
        invoice.save_invoice()
        invoice.calculate_user_debit_credit()
        if setting.update_cost_profit_on_purchase:
            invoice.update_cost_profit()
        return redirect('Invoices:show_invoice', invoice.id)
    context = {
        'form': form,
        'action_url': action_url,
    }
    return render(request, 'Core/form_template.html', context)


def unsave_invoice(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    # invoice.calculate()
    invoice.creator = request.user
    invoice.save()
    action_url = reverse_lazy('Invoices:unsave_invoice', kwargs={'pk': invoice.id})
    form = InvoiceUnSaveForm(request.POST or None, instance=invoice)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        return redirect('Invoices:show_invoice', invoice.id)
    context = {
        'form': form,
        'action_url': action_url,
    }
    return render(request, 'Core/form_template.html', context)


def pay_invoice(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    if invoice.paid and invoice.treasury_in == invoice.overall:
        return render(request, 'empty_base.html', context={'alert': 'هذه الفاتورة مدفوعة بالفعل'})
    if not invoice.invoice_type in [15, 16, 17]:
        if not invoice.customer:
            return render(request, 'empty_base.html', context={'alert': 'يجب اختيار العميل/المورد قبل الحفظ'})
    if invoice.invoice_type in [1, 2, 4, 5, 6]:
        if not invoice.from_treasury and not invoice.to_treasury:
            return render(request, 'empty_base.html', context={'alert': 'يجب اختيار الخزينة قبل الحفظ'})
        if not invoice.from_branch and not invoice.to_branch:
            return render(request, 'empty_base.html', context={'alert': 'يجب اختيار الفرع قبل الحفظ'})

    # invoice.calculate()
    invoice.creator = request.user
    action_url = reverse_lazy('Invoices:pay_invoice', kwargs={'pk': invoice.id})
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
            if TreasuryTransactions.objects.filter(treasury=invoice.from_treasury).exclude(transaction=str(invoice)):
                if invoice.treasury_out > TreasuryTransactions.objects.filter(treasury=invoice.from_treasury).exclude(transaction=str(invoice)).last().balance:
                    if TreasuryTransactions.objects.filter(transaction=str(invoice)):
                        message = 'عفواً لا يوجد رصيد كافٍ داخل الخزينة. الرصيد المتاح: ' + str(TreasuryTransactions.objects.filter(treasury=invoice.from_treasury).last().balance + TreasuryTransactions.objects.get(transaction=str(invoice)).outgoing)
                    else:
                        message = 'عفواً لا يوجد رصيد كافٍ داخل الخزينة. الرصيد المتاح: ' + str(TreasuryTransactions.objects.filter(treasury=invoice.from_treasury).last().balance)
                    messages.add_message(request, messages.ERROR, extra_tags='danger', message=message)
                    return redirect('Invoices:show_invoice', invoice.id)
                form.instance.customer_credit = obj.overall - obj.treasury_out
            else:
                message = 'عفواً لا يوجد رصيد كافٍ داخل الخزينة. الرصيد المتاح: ' + str(0.0)
                messages.add_message(request, messages.ERROR, extra_tags='danger', message=message)
                return redirect('Invoices:show_invoice', invoice.id)
        elif invoice.invoice_type in [1, 2, 3, 6]:
            form.instance.customer_debit = obj.overall - obj.treasury_in
        obj.paid = 1
        obj.save()

        if TreasuryTransactions.objects.filter(transaction=str(invoice)):
            treasury_transactions = TreasuryTransactions.objects.get(transaction=str(invoice))
            money_total_incoming = TreasuryTransactions.objects.filter(treasury=treasury_transactions.treasury).exclude(transaction=str(invoice)).aggregate(totalincoming=Sum('incoming'))
            money_total_outgoing = TreasuryTransactions.objects.filter(treasury=treasury_transactions.treasury).exclude(transaction=str(invoice)).aggregate(totaloutgoing=Sum('outgoing'))
            if invoice.invoice_type in [1, 2, 3, 6]:
                treasury_transactions.incoming = invoice.treasury_in
                treasury_transactions.total_incoming = invoice.treasury_in + money_total_incoming['totalincoming']
                treasury_transactions.total_outgoing = money_total_outgoing['totaloutgoing']
                treasury_transactions.balance = money_total_incoming['totalincoming'] - money_total_outgoing['totaloutgoing'] + invoice.treasury_in
            elif invoice.invoice_type in [4, 5]:
                treasury_transactions.outgoing = invoice.treasury_out
                treasury_transactions.total_outgoing = invoice.treasury_out + money_total_outgoing['totaloutgoing']
                treasury_transactions.total_incoming = money_total_incoming['totalincoming']
                treasury_transactions.balance = money_total_incoming['totalincoming'] - money_total_outgoing['totaloutgoing'] - invoice.treasury_out
            treasury_transactions.save()
        # invoice.save_invoice()
        # if setting.update_cost_profit_on_purchase:
        #     invoice.update_cost_profit()
        return redirect('Invoices:show_invoice', invoice.id)
    context = {
        'form': form,
        'action_url': action_url,
    }
    return render(request, 'Core/form_template.html', context)


def out_invoice(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    if invoice.out_of_warehouse:
        return render(request, 'empty_base.html', context={'alert': 'هذه الفاتورة تمت تسويتها بالفعل'})
    if TreasuryTransactions.objects.filter(treasury=invoice.from_treasury):
        if invoice.treasury_out > TreasuryTransactions.objects.filter(treasury=invoice.from_treasury).last().balance:
            message = 'عفواً لا يوجد رصيد كافٍ داخل الخزينة. الرصيد المتاح: ' + str(TreasuryTransactions.objects.filter(treasury=invoice.from_treasury).last().balance)
            messages.add_message(request, messages.ERROR, extra_tags='danger', message=message)
            return redirect('Invoices:show_invoice', invoice.id)
    action_url = reverse_lazy('Invoices:out_invoice', kwargs={'pk': invoice.id})
    form = OutInvoiceForm(request.POST or None, instance=invoice)
    if form.is_valid():
        form.save()
        invoice.out_of_warehouse = 1
        invoice.creator = request.user
        invoice.save(update_fields=['out_of_warehouse', 'creator'])

        invoice_items = InvoiceItem.objects.filter(invoice=invoice)
        for item in invoice_items:
            profit = 0.0
            # warehouse = None
            # if invoice.from_branch and BranchWarehouses.objects.filter(branch=invoice.from_branch):
            #     warehouse = BranchWarehouses.objects.get(branch=invoice.from_branch)
            # elif invoice.to_branch and BranchWarehouses.objects.filter(branch=invoice.to_branch):
            #     warehouse = BranchWarehouses.objects.get(branch=invoice.to_branch)

            if item.main_unit_main_warehouse > 0:
                if invoice.invoice_type in [4, 5, 16]:
                    warehouse_transactions = WarehouseTransactions()
                    warehouse_transactions.warehouse = invoice.main_warehouse
                    warehouse_transactions.item = item.item
                    warehouse_transactions.incoming = item.main_unit_main_warehouse
                    # warehouse_transactions.purchase_cost = item.item.purchase_price
                    warehouse_transactions.purchase_cost = item.main_unit_price
                    warehouse_transactions.total_incoming = item.main_unit_main_warehouse * item.main_unit_price
                    warehouse_transactions.balance = item.main_unit_main_warehouse
                    warehouse_transactions.save()

                elif invoice.invoice_type in [1, 2, 3, 6, 15]:
                    item_main_ware = invoice.main_warehouse
                    item_main_quant = item.main_unit_main_warehouse

                    if item_main_quant > 0:
                        warehouse_transactions = WarehouseTransactions.objects.filter(item=item.item, warehouse=item_main_ware)
                        for transaction in warehouse_transactions:
                            if item_main_quant > 0:
                                if transaction.balance != 0:
                                    if transaction.balance - item_main_quant < 0:
                                        transaction.outgoing += transaction.balance
                                        transaction.balance = 0
                                        item_main_quant -= transaction.balance
                                    else:
                                        transaction.outgoing += item_main_quant
                                        transaction.balance -= item_main_quant
                                        item_main_quant = 0
                            transaction.save(update_fields=['balance', 'outgoing'])
                            profit += ((transaction.outgoing * item.item.sell_price) - (transaction.outgoing * transaction.purchase_cost))

            if item.main_unit_sub_warehouse > 0:
                if invoice.invoice_type in [4, 5, 16]:
                    warehouse_transactions = WarehouseTransactions()
                    warehouse_transactions.warehouse = invoice.sub_warehouse
                    warehouse_transactions.item = item.item
                    warehouse_transactions.incoming = item.main_unit_sub_warehouse
                    # warehouse_transactions.purchase_cost = item.item.purchase_price
                    warehouse_transactions.purchase_cost = item.main_unit_price
                    warehouse_transactions.total_incoming = item.main_unit_sub_warehouse * item.main_unit_price
                    warehouse_transactions.balance = item.main_unit_sub_warehouse
                    warehouse_transactions.save()

                elif invoice.invoice_type in [1, 2, 3, 6, 15]:
                    item_sub_ware = invoice.sub_warehouse
                    item_sub_quant = item.main_unit_sub_warehouse

                    if item_sub_quant > 0:
                        warehouse_transactions = WarehouseTransactions.objects.filter(item=item.item, warehouse=item_sub_ware)
                        for transaction in warehouse_transactions:
                            if item_sub_quant > 0:
                                if transaction.balance != 0:
                                    if transaction.balance - item_sub_quant < 0:
                                        transaction.outgoing += transaction.balance
                                        transaction.balance = 0
                                        item_sub_quant -= transaction.balance
                                    else:
                                        transaction.outgoing += item_sub_quant
                                        transaction.balance -= item_sub_quant
                                        item_sub_quant = 0
                            transaction.save(update_fields=['balance', 'outgoing'])
                            profit += ((transaction.outgoing * item.item.sell_price) - (transaction.outgoing * transaction.purchase_cost))

            item.profit = profit - item.discount
            item.save()


        if invoice.invoice_type != 15 and invoice.invoice_type != 16 and invoice.invoice_type != 17:
            treasury = None
            if invoice.from_treasury:
                treasury = Treasury.objects.get(id=invoice.from_treasury.id)
            elif invoice.to_treasury:
                treasury = Treasury.objects.get(id=invoice.to_treasury.id)

            money_total_incoming = TreasuryTransactions.objects.filter(treasury=treasury).aggregate(totalincoming=Sum('incoming'))
            money_total_outgoing = TreasuryTransactions.objects.filter(treasury=treasury).aggregate(totaloutgoing=Sum('outgoing'))
            if money_total_incoming['totalincoming'] == None:
                money_total_incoming = 0
            else:
                money_total_incoming = money_total_incoming['totalincoming']

            if money_total_outgoing['totaloutgoing'] == None:
                money_total_outgoing = 0
            else:
                money_total_outgoing = money_total_outgoing['totaloutgoing']

            treasury_transactions = TreasuryTransactions()
            treasury_transactions.transaction = invoice
            treasury_transactions.treasury = treasury
            if invoice.invoice_type in [1, 2, 3, 6]:
                treasury_transactions.incoming = invoice.treasury_in
                treasury_transactions.total_incoming = invoice.treasury_in + money_total_incoming
                treasury_transactions.total_outgoing = money_total_outgoing
                treasury_transactions.balance = money_total_incoming - money_total_outgoing + invoice.treasury_in
            elif invoice.invoice_type in [4, 5]:
                treasury_transactions.outgoing = invoice.treasury_out
                treasury_transactions.total_outgoing = invoice.treasury_out + money_total_outgoing
                treasury_transactions.total_incoming = money_total_incoming
                treasury_transactions.balance = money_total_incoming - money_total_outgoing- invoice.treasury_out
            treasury_transactions.save()

            invoice.calculate_profit()

        return redirect('Invoices:show_invoice', invoice.id)
    context = {
        'form': form,
        'action_url': action_url,
    }
    return render(request, 'Core/form_template.html', context)


def delete_invoice(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    title = "حذف " + invoice.__str__()
    action_url = reverse_lazy('Invoices:delete_invoice', kwargs={'pk': invoice.id})
    form = InvoiceDeleteForm(request.POST or None, instance=invoice)
    if form.is_valid():
        form.save()
        return redirect('Invoices:show_invoice', invoice.id)
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
    return render(request, 'Invoices/OneByOne/opened_invoices.html', context)


def delete_invoice_item(request, pk):
    item = get_object_or_404(InvoiceItem, id=pk)
    invoice = item.invoice
    item.delete()
    invoice.calculate()
    return redirect('Invoices:show_invoice', invoice.id)


def edit_invoice_item_price(request, pk):
    setting = get_invoice_base_setting()
    item = get_object_or_404(InvoiceItem, id=pk)
    invoice = item.invoice
    form = InvoiceItemPriceUpdateForm(request.POST or None, instance=item)
    title = 'تعديل سعر ' + item.item.name
    action_url = reverse_lazy('Invoices:edit_invoice_item_price', kwargs={'pk': item.id})
    if form.is_valid():
        item = form.save(commit=False)
        # if invoice.invoice_type in [1, 2, 6]:
        #     if setting.alert_on_min_cost_price:
        #         if item.unit_price <= item.item.cost_price:
        #             message = 'تنبيه: سعر البيع أقل من سعر التكلفة'
        #             if request.user.has_perm('Invoices.access_purchase_invoice_menu'):
        #                 message += ' سعر التكلفة: ' + str(item.item.cost_price)
        #             messages.add_message(request, messages.WARNING, message)
        #     if setting.alert_on_min_purchase_price:
        #         if item.unit_price <= item.item.purchase_price:
        #             message = 'تنبيه: سعر البيع أقل من سعر الشراء'
        #             if request.user.has_perm('Invoices.access_purchase_invoice_menu'):
        #                 message += ' سعر الشراء: ' + str(item.item.purchase_price)
        #             messages.add_message(request, messages.WARNING, message)

        item.calculate()
        return redirect('Invoices:show_invoice', item.invoice.id)
    context = {
        'title': title,
        'form': form,
        'action_url': action_url,
    }
    return render(request, 'Core/form_template.html', context)


def edit_invoice_item_main_price(request, pk):
    setting = get_invoice_base_setting()
    item = get_object_or_404(InvoiceItem, id=pk)
    invoice = item.invoice
    form = InvoiceItemMainPriceUpdateForm(request.POST or None, instance=item)
    title = 'تعديل سعر ' + item.item.name
    action_url = reverse_lazy('Invoices:edit_invoice_item_price', kwargs={'pk': item.id})
    if form.is_valid():
        item = form.save(commit=False)
        item.unit_price = item.main_unit_price * item.main_unit_quantity
        item.calculate()
        return redirect('Invoices:show_invoice', item.invoice.id)
    context = {
        'title': title,
        'form': form,
        'action_url': action_url,
    }
    return render(request, 'Core/form_template.html', context)


def edit_invoice_item_quantity(request, pk):
    item = get_object_or_404(InvoiceItem, id=pk)
    invoice = item.invoice
    setting = get_invoice_base_setting()
    if invoice.from_branch or invoice.to_branch:
        if invoice.from_branch:
            item_stock = item.item.branch_stock(invoice.from_branch.id)
        if invoice.to_branch:
            item_stock = item.item.branch_stock(invoice.to_branch.id)
    else:
        item_stock = item.item.current_stock()
    form = InvoiceItemQuantityUpdateForm(request.POST or None, instance=item)
    title = 'تعديل كمية ' + item.item.name
    action_url = reverse_lazy('Invoices:edit_invoice_item_quantity', kwargs={'pk': item.id})
    if form.is_valid():
        item = form.save(commit=False)
        if invoice.invoice_type in [1, 2, 6]:
            if not setting.sell_without_stock:
                if not item_stock - item.quantity >= 0:
                    message = 'عفواً لا يوجد رصيد كافٍ. الرصيد المتاح: ' + str(item_stock)
                    messages.add_message(request, messages.ERROR, extra_tags='danger', message=message)
                    return redirect('Invoices:show_invoice', item.invoice.id)
            if setting.alert_on_critical_storage:
                if not item_stock - item.quantity > item.item.critical_stock:
                    message = 'المنتج: ' + item.item.name + ".وصل للرصيد الحرج."
                    messages.add_message(request, messages.WARNING, message)

        form.instance.main_warehouse = item.quantity
        form.instance.sub_warehouse = 0.0
        form.save()
        item.calculate()
        return redirect('Invoices:show_invoice', item.invoice.id)
    context = {
        'title': title,
        'form': form,
        'action_url': action_url,
    }
    return render(request, 'Core/form_template.html', context)


def edit_invoice_item_main_warehouse(request, pk):
    item = get_object_or_404(InvoiceItem, id=pk)
    form = InvoiceItemMainWarehouseUpdateForm(request.POST or None, instance=item)
    title = 'تعديل كمية المخزن الرئيسي ' + item.item.name
    action_url = reverse_lazy('Invoices:edit_invoice_item_main_warehouse', kwargs={'pk': item.id})
    if form.is_valid():
        item = form.save(commit=False)
        form.instance.sub_warehouse = item.quantity - item.main_warehouse
        if item.main_warehouse > item.quantity:
            item.main_warehouse = item.quantity
            item.sub_warehouse = item.quantity - item.main_warehouse
        form.save()
        item.calculate()
        return redirect('Invoices:show_invoice', item.invoice.id)
    context = {
        'title': title,
        'form': form,
        'action_url': action_url,
    }
    return render(request, 'Core/form_template.html', context)


def edit_invoice_item_sub_warehouse(request, pk):
    item = get_object_or_404(InvoiceItem, id=pk)
    form = InvoiceItemSubWarehouseUpdateForm(request.POST or None, instance=item)
    title = 'تعديل كمية المخزن الفرعي ' + item.item.name
    action_url = reverse_lazy('Invoices:edit_invoice_item_sub_warehouse', kwargs={'pk': item.id})
    if form.is_valid():
        item = form.save(commit=False)
        form.instance.main_warehouse = item.quantity - item.sub_warehouse
        if item.sub_warehouse > item.quantity:
            item.sub_warehouse = item.quantity
            item.main_warehouse = item.quantity - item.sub_warehouse
        form.save()
        item.calculate()
        return redirect('Invoices:show_invoice', item.invoice.id)
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
    action_url = reverse_lazy('Invoices:edit_invoice_date', kwargs={'pk': invoice.id})
    if form.is_valid():
        form.save()
        invoice.calculate()
        return redirect('Invoices:show_invoice', invoice.id)
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
    action_url = reverse_lazy('Invoices:edit_invoice_item_discount', kwargs={'pk': item.id})
    if form.is_valid():
        form.save()
        item.calculate()
        return redirect('Invoices:show_invoice', item.invoice.id)
    context = {
        'title': title,
        'form': form,
        'action_url': action_url,
    }
    return render(request, 'Core/form_template.html', context)


def edit_invoice_discount(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    title = 'تعديل خصم فاتورة'
    action_url = reverse_lazy('Invoices:edit_invoice_discount', kwargs={'pk': invoice.id})
    form = InvoiceDiscountUpdateForm(request.POST or None, instance=invoice)
    if form.is_valid():
        invoice2 = form.save(commit=False)
        invoice2.save()
        invoice2.calculate_after_discount()
        invoice.calculate_over_all()
        invoice.calculate_user_debit_credit()
        return redirect('Invoices:show_invoice', invoice.id)
    context = {
        'title': title,
        'action_url': action_url,
        'form': form,
    }
    return render(request, 'Core/form_template.html', context)


def edit_invoice_customer(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    title = 'العميل / مورد'
    action_url = reverse_lazy('Invoices:edit_invoice_customer', kwargs={'pk': invoice.id})
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
        return redirect('Invoices:show_invoice', invoice.id)
    context = {
        'title': title,
        'action_url': action_url,
        'form': form,
    }
    return render(request, 'Core/form_template.html', context)


def edit_invoice_branch(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    title = 'الفرع'
    action_url = reverse_lazy('Invoices:edit_invoice_branch', kwargs={'pk': invoice.id})
    if invoice.invoice_type in [1, 2, 3, 6, 7, 15]:
        form = InvoiceFromBranchForm(request.POST or None, instance=invoice)
        if not request.user.is_superuser:
            form.fields['from_branch'].queryset = request.user.allowed_branches.filter(deleted=False)
        else:
            form.fields['from_branch'].queryset = Branch.objects.filter(deleted=False)
    if invoice.invoice_type in [4, 5, 16]:
        form = InvoiceToBranchForm(request.POST or None, instance=invoice)
        if not request.user.is_superuser:
            form.fields['to_branch'].queryset = request.user.allowed_branches.filter(deleted=False)
        else:
            form.fields['to_branch'].queryset = Branch.objects.filter(deleted=False)
    if invoice.invoice_type == 17:
        form = BranchTransferForm(request.POST or None, instance=invoice)
        if not request.user.is_superuser:
            form.fields['to_branch'].queryset = request.user.allowed_branches.filter(deleted=False)
            form.fields['from_branch'].queryset = request.user.allowed_branches.filter(deleted=False)
        else:
            form.fields['to_branch'].queryset = Branch.objects.filter(deleted=False)
            form.fields['from_branch'].queryset = Branch.objects.filter(deleted=False)

    if form.is_valid():
        invoice = form.save(commit=False)

        if invoice.invoice_type in [1, 2, 3, 6, 7, 15]:
            invoice.main_warehouse = BranchWarehouses.objects.get(branch=invoice.from_branch).main_warehouse
            invoice.sub_warehouse = BranchWarehouses.objects.get(branch=invoice.from_branch).sub_warehouse
        if invoice.invoice_type in [4, 5, 16]:
            invoice.main_warehouse = BranchWarehouses.objects.get(branch=invoice.to_branch).main_warehouse
            invoice.sub_warehouse = BranchWarehouses.objects.get(branch=invoice.to_branch).sub_warehouse

        invoice.save()
        return redirect('Invoices:show_invoice', invoice.id)

    context = {
        'title': title,
        'action_url': action_url,
        'form': form,
    }
    return render(request, 'Core/form_template.html', context)


def edit_invoice_main_warehouse(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    title = 'المخزن الرئيسي للفاتورة'
    action_url = reverse_lazy('Invoices:edit_invoice_main_warehouse', kwargs={'pk': invoice.id})
    form = InvoiceFromMainWarehouseForm(request.POST or None, instance=invoice)
    if invoice.invoice_type in [1, 2, 3, 6, 7, 15]:
        form.fields['main_warehouse'].queryset = Warehouse.objects.filter(Q(branch=invoice.from_branch) | Q(branch=None),deleted=False)
    if invoice.invoice_type in [4, 5, 16]:
        form.fields['main_warehouse'].queryset = Warehouse.objects.filter(Q(branch=invoice.to_branch) | Q(branch=None),deleted=False)
    if form.is_valid():
        invoice = form.save(commit=False)
        invoice.save()
        return redirect('Invoices:show_invoice', invoice.id)

    context = {
        'title': title,
        'action_url': action_url,
        'form': form,
    }
    return render(request, 'Core/form_template.html', context)


def edit_invoice_sub_warehouse(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    title = 'المخزن الفرعي للفاتورة'
    action_url = reverse_lazy('Invoices:edit_invoice_sub_warehouse', kwargs={'pk': invoice.id})
    form = InvoiceFromSubWarehouseForm(request.POST or None, instance=invoice)
    if invoice.invoice_type in [1, 2, 3, 6, 7, 15]:
        form.fields['sub_warehouse'].queryset = Warehouse.objects.filter(Q(branch=invoice.from_branch) | Q(branch=None),deleted=False)
    if invoice.invoice_type in [4, 5, 16]:
        form.fields['sub_warehouse'].queryset = Warehouse.objects.filter(Q(branch=invoice.to_branch) | Q(branch=None),deleted=False)
    if form.is_valid():
        invoice = form.save(commit=False)
        invoice.save()
        return redirect('Invoices:show_invoice', invoice.id)

    context = {
        'title': title,
        'action_url': action_url,
        'form': form,
    }
    return render(request, 'Core/form_template.html', context)


def edit_invoice_warehouse(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    title = 'المخزن'
    action_url = reverse_lazy('Invoices:edit_invoice_warehouse', kwargs={'pk': invoice.id})
    if invoice.invoice_type == 17:
        form = WarehouseTransferForm(request.POST or None, instance=invoice)
        # if not request.user.is_superuser:
        #     form.fields['to_branch'].queryset = request.user.allowed_branches.filter(deleted=False)
        #     form.fields['from_branch'].queryset = request.user.allowed_branches.filter(deleted=False)
        # else:
        #     form.fields['to_branch'].queryset = Branch.objects.filter(deleted=False)
        #     form.fields['from_branch'].queryset = Branch.objects.filter(deleted=False)

    if form.is_valid():
        invoice = form.save(commit=False)
        invoice.save()
        return redirect('Invoices:show_invoice', invoice.id)

    context = {
        'title': title,
        'action_url': action_url,
        'form': form,
    }
    return render(request, 'Core/form_template.html', context)


def edit_invoice_treasury(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    title = 'الخزينة'
    action_url = reverse_lazy('Invoices:edit_invoice_treasury', kwargs={'pk': invoice.id})
    if invoice.invoice_type in [1, 2, 3, 6]:
        form = InvoiceToTreasuryForm(request.POST or None, instance=invoice)
        if not request.user.is_superuser:
            form.fields['to_treasury'].queryset = request.user.allowed_treasuries.filter(Q(branch=invoice.from_branch) | Q(branch=None), deleted=False)
        else:
            form.fields['to_treasury'].queryset = Treasury.objects.filter(Q(branch=invoice.from_branch) | Q(branch=None), deleted=False)
    if invoice.invoice_type in [4, 5]:
        form = InvoiceFromTreasuryForm(request.POST or None, instance=invoice)
        if not request.user.is_superuser:
            form.fields['from_treasury'].queryset = request.user.allowed_treasuries.filter(Q(branch=invoice.to_branch) | Q(branch=None), deleted=False)
        else:
            form.fields['from_treasury'].queryset = Treasury.objects.filter(Q(branch=invoice.to_branch) | Q(branch=None), deleted=False)

    if form.is_valid():
        invoice = form.save(commit=False)
        invoice.save()
        return redirect('Invoices:show_invoice', invoice.id)
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
    if cust:
        customer = get_object_or_404(Customer, id=cust.id)

        if invoice.invoice_type in [1, 2, 3, 4, 7]:
            cat = customer.sales_category
        if invoice.invoice_type in [5, 6]:
            cat = customer.purchases_category

        category = None
        if cat:
            category = get_object_or_404(Category, id=cat.id)

        prod_price = ProductPrices.objects.filter(inactive=False, deleted=False, product=product, customer_segment=category)

        if prod_price:
            product_price = ProductPrices.objects.get(inactive=False, deleted=False, product=product, customer_segment=category).price
        else:
            if invoice.invoice_type in [1, 2, 3, 4, 7]:
                product_price = product.sell_price
            if invoice.invoice_type in [5, 6]:
                product_price = product.purchase_price
    else:
        if invoice.invoice_type in [1, 2, 3, 4, 7]:
            product_price = product.sell_price
        if invoice.invoice_type in [5, 6]:
            product_price = product.purchase_price

    return HttpResponse(product_price)


def get_form_main_warehouse(request, invoice_id):
    myarr = request.GET.get('myarr').split(',')

    invoice = get_object_or_404(Invoice, id=invoice_id)
    # warehouse = None
    # if invoice.from_branch and BranchWarehouses.objects.filter(branch=invoice.from_branch):
    #     warehouse = BranchWarehouses.objects.get(branch=invoice.from_branch)
    # elif invoice.to_branch and BranchWarehouses.objects.filter(branch=invoice.to_branch):
    #     warehouse = BranchWarehouses.objects.get(branch=invoice.to_branch)

    main_items = WarehouseTransactions.objects.filter(item_id=int(myarr[0]), warehouse=invoice.main_warehouse).aggregate(total=Sum('balance'))
    # all_main_items = main_items['total']
    unit = get_object_or_404(Unit, id=int(myarr[1]))
    if ProductUnit.objects.filter(product_id=int(myarr[0]), unit_name=unit):
        unit_count = get_unit_count(int(myarr[0]), int(myarr[1]))
        all_main_items = main_items['total'] / unit_count
    else:
        all_main_items = main_items['total']
    return HttpResponse(all_main_items)


def get_form_sub_warehouse(request, invoice_id):
    myarr = request.GET.get('myarr').split(',')

    invoice = get_object_or_404(Invoice, id=invoice_id)
    # warehouse = None
    # if invoice.from_branch and BranchWarehouses.objects.filter(branch=invoice.from_branch):
    #     warehouse = BranchWarehouses.objects.get(branch=invoice.from_branch)
    # elif invoice.to_branch and BranchWarehouses.objects.filter(branch=invoice.to_branch):
    #     warehouse = BranchWarehouses.objects.get(branch=invoice.to_branch)
    sub_items = WarehouseTransactions.objects.filter(item_id=int(myarr[0]), warehouse=invoice.sub_warehouse).aggregate(total=Sum('balance'))
    # all_sub_items = sub_items['total']

    unit = get_object_or_404(Unit, id=int(myarr[1]))
    if ProductUnit.objects.filter(product_id=int(myarr[0]), unit_name=unit):
        unit_count = get_unit_count(int(myarr[0]), int(myarr[1]))
        all_sub_items = sub_items['total'] / unit_count
    else:
        all_sub_items = sub_items['total']

    return HttpResponse(all_sub_items)


def get_form_all_warehouse(request, invoice_id):
    myarr = request.GET.get('myarr').split(',')
    items = WarehouseTransactions.objects.filter(item_id=int(myarr[0])).aggregate(total=Sum('balance'))
    unit = get_object_or_404(Unit, id=int(myarr[1]))
    if ProductUnit.objects.filter(product_id=int(myarr[0]), unit_name=unit):
        # product_unit = ProductUnit.objects.get(product_id=int(myarr[0]), unit_name=unit)
        # all_items = items['total'] / product_unit.unit_quantity
        unit_count = get_unit_count(int(myarr[0]), int(myarr[1]))
        all_items = items['total'] / unit_count
    else:
        all_items = items['total']

    return HttpResponse(all_items)


def get_product_sell_comment(request):
    product = get_object_or_404(Product, id=request.GET.get('product_id'))
    return HttpResponse(product.sales_man_comment)


def get_customer_sell_comment(request):
    customer = get_object_or_404(Customer, id=request.GET.get('customer_id'))
    return HttpResponse(customer.seller_feedback)


def get_product_units(request):
    if request.is_ajax():
        product = get_object_or_404(Product, id=request.GET.get('product_id'))
        produc_units = ProductUnit.objects.filter(product=product, deleted=0)
        # form = InvoiceItemForm(request.POST or None)
        # form.fields['unit_name'].queryset = produc_units
        return render(request, 'Invoices/OneByOne/product_units_filter.html', {'produc_units': produc_units, 'product':product})


def display_all_prods(request):
    if request.is_ajax():
        products = Product.objects.filter(deleted=False)
        return render(request, 'Invoices/OneByOne/display_all_prods_filter.html', {'products': products})


def get_unit_count(product_id, unit_id):
    product_item = get_object_or_404(Product, id=int(product_id))
    unit_item = get_object_or_404(Unit, id=int(unit_id))
    product_units = ProductUnit.objects.get(unit_name=unit_item, product=product_item, deleted=0)
    # return product_units.unit_quantity

    ##########################################################
    units = {}
    units_1 = []
    u = 1.0
    y = 1.0
    product_units_1 = ProductUnit.objects.filter(Q(unit_name=product_item.main_unit) | Q(unit_from=product_item.main_unit), product=product_item, deleted=0)
    product_units_2 = ProductUnit.objects.filter(~Q(unit_name=product_item.main_unit), ~Q(unit_from=product_item.main_unit), product=product_item, deleted=0)
    product_units_all = ProductUnit.objects.filter(product=product_item, deleted=0)

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

    return units[product_units.id]
    ###############################################################




def get_unit_all_price(request, invoice_id):
    myarr = request.GET.get('myarr').split(',')

    product = get_object_or_404(Product, id=int(myarr[0]))
    unit = get_object_or_404(Unit, id=int(myarr[1]))
    product_price = myarr[2]

    product_main_unit = product.main_unit

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

def expense_invoice(request):
    title = 'إذن صرف نقدية'
    form = ExpenseInvoiceForm(request.POST or None)
    if not request.user.is_superuser:
        form.fields['treasury'].querset = request.user.allowed_treasuries.all()
        if not request.user.has_perm('Invoices.edit_invoice_date'):
            form.fields['date'].disabled = True
    form.initial['treasury'] = request.user.default_treasury
    action_url = reverse_lazy('Invoices:expense_invoice')
    if form.is_valid():
        obj = form.save(commit=False)
        obj.invoice_type = 11
        obj.creator = request.user
        obj.saved = True
        obj.save()

        invoice = get_object_or_404(Invoice, id=obj.id)
        if invoice.invoice_type == 11:
            from_treasery = get_object_or_404(Treasury, id=invoice.from_treasury.id)

            money_total_incoming_f = TreasuryTransactions.objects.filter(treasury=from_treasery).aggregate(totalincoming=Sum('incoming'))
            money_total_outgoing_f = TreasuryTransactions.objects.filter(treasury=from_treasery).aggregate(totaloutgoing=Sum('outgoing'))


            if money_total_incoming_f['totalincoming'] == None:
                money_total_incoming_f = 0
            else:
                money_total_incoming_f = money_total_incoming_f['totalincoming']

            if money_total_outgoing_f['totaloutgoing'] == None:
                money_total_outgoing_f = 0
            else:
                money_total_outgoing_f = money_total_outgoing_f['totaloutgoing']

            treasury_transactions_f = TreasuryTransactions()
            treasury_transactions_f.transaction = obj
            treasury_transactions_f.treasury = from_treasery
            treasury_transactions_f.outgoing = obj.treasury_out
            treasury_transactions_f.total_outgoing = obj.treasury_out + money_total_outgoing_f
            treasury_transactions_f.total_incoming = money_total_incoming_f
            treasury_transactions_f.balance = money_total_incoming_f - money_total_outgoing_f - obj.treasury_out
            treasury_transactions_f.save()

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
        form.fields['treasury'].querset = request.user.allowed_treasuries.all()
        if not request.user.has_perm('Invoices.edit_invoice_date'):
            form.fields['date'].disabled = True
    action_url = reverse_lazy('Invoices:edit_fast_invoice', kwargs={'pk': invoice.id})
    if form.is_valid():
        obj = form.save(commit=False)
        if invoice.invoice_type == 19:
            obj.treasury_out = form.cleaned_data['treasury_in']
        obj.saved = True
        obj.save()

        if invoice.invoice_type == 19 or invoice.invoice_type == 11 or invoice.invoice_type == 12 or invoice.invoice_type == 13 or invoice.invoice_type == 14:
            from_treasery = None
            to_treasery = None
            money_total_incoming_f = None
            money_total_outgoing_f = None
            money_total_incoming_t = None
            money_total_outgoing_t = None
            if invoice.invoice_type == 19 or invoice.invoice_type == 11 or invoice.invoice_type == 13:
                from_treasery = get_object_or_404(Treasury, id=invoice.from_treasury.id)
            if invoice.invoice_type == 19 or invoice.invoice_type == 12 or invoice.invoice_type == 14:
                to_treasery = get_object_or_404(Treasury, id=invoice.to_treasury.id)

            if invoice.invoice_type == 19 or invoice.invoice_type == 11 or invoice.invoice_type == 13:
                money_total_incoming_f = TreasuryTransactions.objects.filter(treasury=from_treasery).aggregate(totalincoming=Sum('incoming'))
                money_total_outgoing_f = TreasuryTransactions.objects.filter(treasury=from_treasery).aggregate(totaloutgoing=Sum('outgoing'))

            if invoice.invoice_type == 19 or invoice.invoice_type == 12 or invoice.invoice_type == 14:
                money_total_incoming_t = TreasuryTransactions.objects.filter(treasury=to_treasery).aggregate(totalincoming=Sum('incoming'))
                money_total_outgoing_t = TreasuryTransactions.objects.filter(treasury=to_treasery).aggregate(totaloutgoing=Sum('outgoing'))

            if invoice.invoice_type == 19 or invoice.invoice_type == 11 or invoice.invoice_type == 13:
                if money_total_incoming_f['totalincoming'] == None:
                    money_total_incoming_f = 0
                else:
                    money_total_incoming_f = money_total_incoming_f['totalincoming']

                if money_total_outgoing_f['totaloutgoing'] == None:
                    money_total_outgoing_f = 0
                else:
                    money_total_outgoing_f = money_total_outgoing_f['totaloutgoing']

            if invoice.invoice_type == 19 or invoice.invoice_type == 12 or invoice.invoice_type == 14:
                if money_total_incoming_t['totalincoming'] == None:
                    money_total_incoming_t = 0
                else:
                    money_total_incoming_t = money_total_incoming_t['totalincoming']

                if money_total_outgoing_t['totaloutgoing'] == None:
                    money_total_outgoing_t = 0
                else:
                    money_total_outgoing_t = money_total_outgoing_t['totaloutgoing']

            if invoice.invoice_type == 19 or invoice.invoice_type == 11 or invoice.invoice_type == 13:
                if TreasuryTransactions.objects.filter(transaction=str(obj)):
                    treasury_transactions_f = TreasuryTransactions.objects.get(transaction=str(obj))
                    money_total_incoming_f = TreasuryTransactions.objects.filter(treasury=from_treasery).exclude(id=treasury_transactions_f.id).aggregate(totalincoming=Sum('incoming'))
                    money_total_outgoing_f = TreasuryTransactions.objects.filter(treasury=from_treasery).exclude(id=treasury_transactions_f.id).aggregate(totaloutgoing=Sum('outgoing'))
                    if money_total_incoming_f['totalincoming'] == None:
                        money_total_incoming_f = 0
                    else:
                        money_total_incoming_f = money_total_incoming_f['totalincoming']

                    if money_total_outgoing_f['totaloutgoing'] == None:
                        money_total_outgoing_f = 0
                    else:
                        money_total_outgoing_f = money_total_outgoing_f['totaloutgoing']
                else:
                    treasury_transactions_f = TreasuryTransactions()

                if invoice.invoice_type == 19 and not TreasuryTransactions.objects.filter(transaction=str(obj)):
                    treasury_transactions_f.transaction = obj
                if invoice.invoice_type == 11 and not TreasuryTransactions.objects.filter(transaction=str(obj)):
                    treasury_transactions_f.transaction = obj
                if invoice.invoice_type == 13 and not TreasuryTransactions.objects.filter(transaction=str(obj)):
                    treasury_transactions_f.transaction = obj

                treasury_transactions_f.treasury = from_treasery
                if invoice.invoice_type == 19:
                    treasury_transactions_f.outgoing = obj.treasury_in
                    treasury_transactions_f.total_outgoing = obj.treasury_in + money_total_outgoing_f
                    treasury_transactions_f.total_incoming = money_total_incoming_f
                    treasury_transactions_f.balance = money_total_incoming_f - money_total_outgoing_f - obj.treasury_in
                if invoice.invoice_type == 11 or invoice.invoice_type == 13:
                    treasury_transactions_f.outgoing = obj.treasury_out
                    treasury_transactions_f.total_outgoing = obj.treasury_out + money_total_outgoing_f
                    treasury_transactions_f.total_incoming = money_total_incoming_f
                    treasury_transactions_f.balance = money_total_incoming_f - money_total_outgoing_f - obj.treasury_out
                treasury_transactions_f.save()

            if invoice.invoice_type == 19 or invoice.invoice_type == 12 or invoice.invoice_type == 14:
                if TreasuryTransactions.objects.filter(transaction=str(obj)):
                    treasury_transactions_t = TreasuryTransactions.objects.get(transaction=str(obj))
                    money_total_incoming_t = TreasuryTransactions.objects.filter(treasury=to_treasery).exclude(id=treasury_transactions_t.id).aggregate(totalincoming=Sum('incoming'))
                    money_total_outgoing_t = TreasuryTransactions.objects.filter(treasury=to_treasery).exclude(id=treasury_transactions_t.id).aggregate(totaloutgoing=Sum('outgoing'))
                    if money_total_incoming_t['totalincoming'] == None:
                        money_total_incoming_t = 0
                    else:
                        money_total_incoming_t = money_total_incoming_t['totalincoming']

                    if money_total_outgoing_t['totaloutgoing'] == None:
                        money_total_outgoing_t = 0
                    else:
                        money_total_outgoing_t = money_total_outgoing_t['totaloutgoing']
                else:
                    treasury_transactions_t = TreasuryTransactions()

                if invoice.invoice_type == 19 and not TreasuryTransactions.objects.filter(transaction=str(obj)):
                    treasury_transactions_t.transaction = obj
                if invoice.invoice_type == 12 and not TreasuryTransactions.objects.filter(transaction=str(obj)):
                    treasury_transactions_t.transaction = obj
                if invoice.invoice_type == 14 and not TreasuryTransactions.objects.filter(transaction=str(obj)):
                    treasury_transactions_t.transaction = obj

                treasury_transactions_t.treasury = to_treasery
                treasury_transactions_t.incoming = obj.treasury_in
                treasury_transactions_t.total_incoming = obj.treasury_in + money_total_incoming_t
                treasury_transactions_t.total_outgoing = money_total_outgoing_t
                treasury_transactions_t.balance = money_total_incoming_t - money_total_outgoing_t + obj.treasury_in
                treasury_transactions_t.save()

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
    action_url = reverse_lazy('Invoices:income_invoice')
    if form.is_valid():
        obj = form.save(commit=False)
        obj.invoice_type = 12
        obj.creator = request.user
        obj.saved = True
        obj.save()

        invoice = get_object_or_404(Invoice, id=obj.id)
        if invoice.invoice_type == 12:
            to_treasery = get_object_or_404(Treasury, id=invoice.to_treasury.id)

            money_total_incoming_t = TreasuryTransactions.objects.filter(treasury=to_treasery).aggregate(totalincoming=Sum('incoming'))
            money_total_outgoing_t = TreasuryTransactions.objects.filter(treasury=to_treasery).aggregate(totaloutgoing=Sum('outgoing'))

            if money_total_incoming_t['totalincoming'] == None:
                money_total_incoming_t = 0
            else:
                money_total_incoming_t = money_total_incoming_t['totalincoming']

            if money_total_outgoing_t['totaloutgoing'] == None:
                money_total_outgoing_t = 0
            else:
                money_total_outgoing_t = money_total_outgoing_t['totaloutgoing']

            treasury_transactions_t = TreasuryTransactions()
            treasury_transactions_t.transaction = obj
            treasury_transactions_t.treasury = to_treasery
            treasury_transactions_t.incoming = obj.treasury_in
            treasury_transactions_t.total_incoming = obj.treasury_in + money_total_incoming_t
            treasury_transactions_t.total_outgoing = money_total_outgoing_t
            treasury_transactions_t.balance = money_total_incoming_t - money_total_outgoing_t + obj.treasury_in
            treasury_transactions_t.save()

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
        return redirect('Invoices:show_invoice', last_invoice.id)
    else:
        return redirect('Invoices:show_opened_invoices', int(type))


def search_invoice(request):
    id = request.GET.get('invoice_id')
    invoice = get_object_or_404(Invoice, id=id)
    return redirect('Invoices:show_invoice', invoice.id)


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
    return render(request, 'Invoices/Print/' + str(setting.size) + '.html', context)


def customer_income(request):
    title = 'إذن قبض سداد'
    form = CustomerIncomeForm(request.POST or None)
    if request.GET.get('customer'):
        customer = get_object_or_404(Customer, id=request.GET.get('customer'))
        form.initial['customer'] = customer
    if not request.user.is_superuser:
        form.fields['treasury'].querset = request.user.allowed_treasuries.all()
    form.initial['treasury'] = request.user.default_treasury
    action_url = reverse_lazy('Invoices:income_invoice')
    if form.is_valid():
        obj = form.save(commit=False)
        obj.invoice_type = 21
        obj.creator = request.user
        obj.saved = True
        obj.save()
        obj.calculate()
        url = request.POST.get('url')
        return redirect(url)
    context = {
        'title': title,
        'form': form,
        'action_url': action_url,
    }
    return render(request, 'Core/form_template.html', context)


def customer_outcome(request):
    title = 'إذن صرف سداد'
    form = CustomerOutcomeForm(request.POST or None)
    if request.GET.get('customer'):
        customer = get_object_or_404(Customer, id=request.GET.get('customer'))
        form.initial['customer'] = customer
    if not request.user.is_superuser:
        form.fields['treasury'].querset = request.user.allowed_treasuries.all()
    form.initial['treasury'] = request.user.default_treasury
    action_url = reverse_lazy('Invoices:income_invoice')
    if form.is_valid():
        obj = form.save(commit=False)
        obj.invoice_type = 22
        obj.creator = request.user
        obj.saved = True
        obj.save()
        obj.calculate()
        url = request.POST.get('url')
        return redirect(url)
    context = {
        'title': title,
        'form': form,
        'action_url': action_url,
    }
    return render(request, 'Core/form_template.html', context)


def capital_plus(request):
    title = 'إضافة لرأس المال'
    form = CapitalIncomeForm(request.POST or None)
    if not request.user.is_superuser:
        form.fields['to_treasury'].querset = request.user.allowed_treasuries.all()
        if not request.user.has_perm('Invoices.edit_invoice_date'):
            form.fields['date'].disabled = True
    form.initial['to_treasury'] = request.user.default_treasury
    action_url = reverse_lazy('Invoices:capital_plus')
    if form.is_valid():
        obj = form.save(commit=False)
        obj.invoice_type = 13
        obj.creator = request.user
        obj.saved = True
        obj.save()

        invoice = get_object_or_404(Invoice, id=obj.id)
        if invoice.invoice_type == 14:
            to_treasery = get_object_or_404(Treasury, id=invoice.to_treasury.id)

            money_total_incoming_t = TreasuryTransactions.objects.filter(treasury=to_treasery).aggregate(
                totalincoming=Sum('incoming'))
            money_total_outgoing_t = TreasuryTransactions.objects.filter(treasury=to_treasery).aggregate(
                totaloutgoing=Sum('outgoing'))

            if money_total_incoming_t['totalincoming'] == None:
                money_total_incoming_t = 0
            else:
                money_total_incoming_t = money_total_incoming_t['totalincoming']

            if money_total_outgoing_t['totaloutgoing'] == None:
                money_total_outgoing_t = 0
            else:
                money_total_outgoing_t = money_total_outgoing_t['totaloutgoing']

            treasury_transactions_t = TreasuryTransactions()
            treasury_transactions_t.transaction = obj
            treasury_transactions_t.treasury = to_treasery
            treasury_transactions_t.incoming = obj.treasury_in
            treasury_transactions_t.total_incoming = obj.treasury_in + money_total_incoming_t
            treasury_transactions_t.total_outgoing = money_total_outgoing_t
            treasury_transactions_t.balance = money_total_incoming_t - money_total_outgoing_t + obj.treasury_in
            treasury_transactions_t.save()

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
        form.fields['from_treasury'].querset = request.user.allowed_treasuries.all()
        if not request.user.has_perm('Invoices.edit_invoice_date'):
            form.fields['date'].disabled = True
    form.initial['from_treasury'] = request.user.default_treasury
    action_url = reverse_lazy('Invoices:capital_minus')
    if form.is_valid():
        obj = form.save(commit=False)
        obj.invoice_type = 14
        obj.creator = request.user
        obj.saved = True
        obj.save()

        invoice = get_object_or_404(Invoice, id=obj.id)
        if invoice.invoice_type == 13:
            from_treasery = get_object_or_404(Treasury, id=invoice.from_treasury.id)

            money_total_incoming_f = TreasuryTransactions.objects.filter(treasury=from_treasery).aggregate(
                totalincoming=Sum('incoming'))
            money_total_outgoing_f = TreasuryTransactions.objects.filter(treasury=from_treasery).aggregate(
                totaloutgoing=Sum('outgoing'))

            if money_total_incoming_f['totalincoming'] == None:
                money_total_incoming_f = 0
            else:
                money_total_incoming_f = money_total_incoming_f['totalincoming']

            if money_total_outgoing_f['totaloutgoing'] == None:
                money_total_outgoing_f = 0
            else:
                money_total_outgoing_f = money_total_outgoing_f['totaloutgoing']

            treasury_transactions_f = TreasuryTransactions()
            treasury_transactions_f.transaction = obj
            treasury_transactions_f.treasury = from_treasery
            treasury_transactions_f.outgoing = obj.treasury_out
            treasury_transactions_f.total_outgoing = obj.treasury_out + money_total_outgoing_f
            treasury_transactions_f.total_incoming = money_total_incoming_f
            treasury_transactions_f.balance = money_total_incoming_f - money_total_outgoing_f - obj.treasury_out
            treasury_transactions_f.save()

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
    if next_invoice:
        return redirect(reverse_lazy('Invoices:show_invoice', kwargs={'pk': next_invoice.id}))
    elif prev_invoice:
        return redirect(reverse_lazy('Invoices:show_invoice', kwargs={'pk': prev_invoice.id}))
    else:
        return redirect(reverse_lazy('Invoices:get_last_invoice', kwargs={'type': invoice_type}))


def treasury_transfer(request):
    title = 'تحويل خزينة'
    form = TreasuryTransferForm(request.POST or None)
    if form.is_valid():
        invoice = form.save(commit=False)
        invoice.invoice_type = 19
        invoice.treasury_out = form.cleaned_data['treasury_in']
        invoice.saved = True
        invoice.creator = request.user
        invoice.save()

        if invoice.invoice_type == 19:
            from_treasery = get_object_or_404(Treasury, id=invoice.from_treasury.id)
            to_treasery = get_object_or_404(Treasury, id=invoice.to_treasury.id)

            money_total_incoming_f = TreasuryTransactions.objects.filter(treasury=from_treasery).aggregate(totalincoming=Sum('incoming'))
            money_total_outgoing_f = TreasuryTransactions.objects.filter(treasury=from_treasery).aggregate(totaloutgoing=Sum('outgoing'))

            money_total_incoming_t = TreasuryTransactions.objects.filter(treasury=to_treasery).aggregate(totalincoming=Sum('incoming'))
            money_total_outgoing_t = TreasuryTransactions.objects.filter(treasury=to_treasery).aggregate(totaloutgoing=Sum('outgoing'))

            if money_total_incoming_f['totalincoming'] == None:
                money_total_incoming_f = 0
            else:
                money_total_incoming_f = money_total_incoming_f['totalincoming']

            if money_total_outgoing_f['totaloutgoing'] == None:
                money_total_outgoing_f = 0
            else:
                money_total_outgoing_f = money_total_outgoing_f['totaloutgoing']

            if money_total_incoming_t['totalincoming'] == None:
                money_total_incoming_t = 0
            else:
                money_total_incoming_t = money_total_incoming_t['totalincoming']

            if money_total_outgoing_t['totaloutgoing'] == None:
                money_total_outgoing_t = 0
            else:
                money_total_outgoing_t = money_total_outgoing_t['totaloutgoing']

            treasury_transactions_f = TreasuryTransactions()
            treasury_transactions_f.transaction = invoice
            treasury_transactions_f.treasury = from_treasery
            treasury_transactions_f.outgoing = invoice.treasury_in
            treasury_transactions_f.total_outgoing = invoice.treasury_in + money_total_outgoing_f
            treasury_transactions_f.total_incoming = money_total_incoming_f
            treasury_transactions_f.balance = money_total_incoming_f - money_total_outgoing_f - invoice.treasury_in
            treasury_transactions_f.save()

            treasury_transactions_t = TreasuryTransactions()
            treasury_transactions_t.transaction = invoice
            treasury_transactions_t.treasury = to_treasery
            treasury_transactions_t.incoming = invoice.treasury_in
            treasury_transactions_t.total_incoming = invoice.treasury_in + money_total_incoming_t
            treasury_transactions_t.total_outgoing = money_total_outgoing_t
            treasury_transactions_t.balance = money_total_incoming_t - money_total_outgoing_t + invoice.treasury_in
            treasury_transactions_t.save()

        url = request.POST.get('url')
        return redirect(url)
    context = {
        'title': title,
        'form': form,
    }
    return render(request, 'Core/form_template.html', context)


class SpendCategoryList(ListView):
    model = SpendCategory
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        return queryset


class SpendCategoryTrashList(ListView):
    model = SpendCategory
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True)
        if self.request.GET.get('id'):
            queryset = queryset.filter(id=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            queryset = queryset.filter(name__icontains=self.request.GET.get('name'))
        return queryset


class SpendCategoryCreate(CreateView):
    model = SpendCategory
    form_class = SpendCategoryForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Invoices:SpendCategoryList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة تصنيف مصروفات'
        context['action_url'] = reverse_lazy('Invoices:SpendCategoryCreate')
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class SpendCategoryUpdate(UpdateView):
    model = SpendCategory
    form_class = SpendCategoryForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Invoices:SpendCategoryList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل تصنيف مصروفات: ' + str(self.object)
        context['action_url'] = reverse_lazy('Invoices:SpendCategoryUpdate', kwargs={'pk': self.object.id})
        return context


class SpendCategoryDelete(UpdateView):
    model = SpendCategory
    form_class = SpendCategoryDeleteForm
    template_name = 'Core/form_template.html'
    success_url = reverse_lazy('Invoices:SpendCategoryList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف تصنيف مصروفات: ' + str(self.object)
        context['action_url'] = reverse_lazy('Invoices:SpendCategoryDelete', kwargs={'pk': self.object.id})
        return context


def add_customer_to_invoice(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    form = CustomerForm(request.POST or None)
    if form.is_valid():
        customer = form.save(commit=False)
        customer.save()
        invoice.customer = customer
        invoice.save()
        return redirect('Invoices:show_invoice', pk)
    context = {
        'title': 'إضافة عميل / مورد',
        'form': form,
    }
    return render(request, 'Core/form_template.html', context)


def add_product_to_invoice(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    form = InvoiceItemForm(request.POST or None)

    if form.is_valid():
        prod = form.save(commit=False)
        form.instance.invoice = invoice
        form.instance.profit = 0
        form.instance.main_unit_quantity = 0
        form.instance.main_unit_main_warehouse = 0
        form.instance.main_unit_sub_warehouse = 0
        prod.save()
        invoice_item = get_object_or_404(InvoiceItem, id=prod.id)
        invoice_item.calculate()
        # invoice_item.calculate_profit()

        invoice_item.calculate_main_units()
        # warehouse = None
        # if invoice.from_branch and BranchWarehouses.objects.filter(branch=invoice.from_branch):
        #     warehouse = BranchWarehouses.objects.get(branch=invoice.from_branch)
        # elif invoice.to_branch and BranchWarehouses.objects.filter(branch=invoice.to_branch):
        #     warehouse = BranchWarehouses.objects.get(branch=invoice.to_branch)

        if invoice.invoice_type in [1, 2, 6]:
            warehouse_main_warehouse = WarehouseTransactions.objects.filter(item=invoice_item.item,warehouse=invoice.main_warehouse)
            warehouse_sub_warehouse = WarehouseTransactions.objects.filter(item=invoice_item.item,warehouse=invoice.sub_warehouse)
            item_main_warehouse_balance = 0.0
            item_sub_warehouse_balance = 0.0
            if warehouse_main_warehouse:
                item_main_warehouse_balance = warehouse_main_warehouse.aggregate(balance=Sum('balance'))
            if warehouse_sub_warehouse:
                item_sub_warehouse_balance = warehouse_sub_warehouse.aggregate(balance=Sum('balance'))

            if warehouse_main_warehouse and item_main_warehouse_balance['balance'] == 0.0:
                item_main_warehouse_balance = 0.0
            else:
                item_main_warehouse_balance = float(item_main_warehouse_balance['balance'])

            if warehouse_sub_warehouse and item_sub_warehouse_balance['balance'] == 0.0:
                item_sub_warehouse_balance = 0.0
            else:
                item_sub_warehouse_balance = float(item_sub_warehouse_balance['balance'])

            if warehouse_main_warehouse and warehouse_sub_warehouse:
                if invoice_item.main_unit_quantity > float(item_main_warehouse_balance + item_sub_warehouse_balance):
                    invoice_item.delete()
                    message = 'عفواً لا يوجد رصيد كافٍ داخل المخازن. الرصيد المتاح: ' + str(item_main_warehouse_balance + item_sub_warehouse_balance)
                    messages.add_message(request, messages.ERROR, extra_tags='danger', message=message)
                    return redirect('Invoices:show_invoice', invoice.id)
                    # return HttpResponse(message)
            else:
                invoice_item.delete()
                message = 'عفواً لا يوجد رصيد كافٍ داخل المخازن. الرصيد المتاح: ' + str(0.0)
                messages.add_message(request, messages.ERROR, extra_tags='danger', message=message)
                return redirect('Invoices:show_invoice', invoice.id)
                # return HttpResponse(message)

            if warehouse_main_warehouse:
                if invoice_item.main_unit_main_warehouse > float(item_main_warehouse_balance):
                    invoice_item.delete()
                    message = 'عفواً لا يوجد رصيد كافٍ داخل المخزن الرئيسي. الرصيد المتاح: ' + str(item_main_warehouse_balance)
                    messages.add_message(request, messages.ERROR, extra_tags='danger', message=message)
                    return redirect('Invoices:show_invoice', invoice.id)
                    # return HttpResponse(message)

            if warehouse_sub_warehouse:
                if invoice_item.main_unit_sub_warehouse > float(item_sub_warehouse_balance):
                    invoice_item.delete()
                    message = 'عفواً لاتوجد كمية كافية داخل المخزن الفرعي. الكمية المتاحة: ' + str(item_sub_warehouse_balance)
                    messages.add_message(request, messages.ERROR, extra_tags='danger', message=message)
                    return redirect('Invoices:show_invoice', invoice.id)
                    # return HttpResponse(message)

    return redirect('Invoices:show_invoice', invoice.id)

# def add_product_to_invoice(request, pk):
#     invoice = get_object_or_404(Invoice, id=pk)
#     form = InvoiceItemForm(request.POST or None)
#
#     if form.is_valid():
#         prod = form.save(commit=False)
#         form.instance.invoice = invoice
#         form.instance.profit = 0
#         form.instance.main_unit_quantity = 0
#         form.instance.main_unit_main_warehouse = 0
#         form.instance.main_unit_sub_warehouse = 0
#         prod.save()
#         invoice_item = get_object_or_404(InvoiceItem, id=prod.id)
#         invoice_item.calculate()
#         invoice_item.calculate_profit()
#
#         invoice_item.calculate_main_units()
#         warehouse = None
#         if invoice.from_branch and BranchWarehouses.objects.filter(branch=invoice.from_branch):
#             warehouse = BranchWarehouses.objects.get(branch=invoice.from_branch)
#         elif invoice.to_branch and BranchWarehouses.objects.filter(branch=invoice.to_branch):
#             warehouse = BranchWarehouses.objects.get(branch=invoice.to_branch)
#         if invoice.invoice_type in [1, 2, 6]:
#             if WarehouseTransactions.objects.filter(item=invoice_item.item, warehouse=warehouse.main_warehouse) and WarehouseTransactions.objects.filter(item=invoice_item.item, warehouse=warehouse.sub_warehouse):
#                 if invoice_item.main_unit_quantity > float(WarehouseTransactions.objects.filter(item=invoice_item.item, warehouse=warehouse.main_warehouse).last().balance + WarehouseTransactions.objects.filter(item=invoice_item.item, warehouse=warehouse.sub_warehouse).last().balance):
#                     invoice_item.delete()
#                     message = 'عفواً لا يوجد رصيد كافٍ داخل المخازن. الرصيد المتاح: ' + str(WarehouseTransactions.objects.filter(item=invoice_item.item, warehouse=warehouse.main_warehouse).last().balance + WarehouseTransactions.objects.filter(item=invoice_item.item, warehouse=warehouse.sub_warehouse).last().balance)
#                     messages.add_message(request, messages.ERROR, extra_tags='danger', message=message)
#                     return redirect('Invoices:show_invoice', invoice.id)
#             else:
#                 invoice_item.delete()
#                 message = 'عفواً لا يوجد رصيد كافٍ داخل المخازن. الرصيد المتاح: ' + str(0.0)
#                 messages.add_message(request, messages.ERROR, extra_tags='danger', message=message)
#                 return redirect('Invoices:show_invoice', invoice.id)
#
#             if WarehouseTransactions.objects.filter(item=invoice_item.item, warehouse=warehouse.main_warehouse):
#                 if invoice_item.main_unit_main_warehouse > WarehouseTransactions.objects.filter(item=invoice_item.item, warehouse=warehouse.main_warehouse).last().balance:
#                     invoice_item.delete()
#                     message = 'عفواً لا يوجد رصيد كافٍ داخل المخزن الرئيسي. الرصيد المتاح: ' + str(WarehouseTransactions.objects.filter(item=invoice_item.item, warehouse=warehouse.main_warehouse).last().balance)
#                     messages.add_message(request, messages.ERROR, extra_tags='danger', message=message)
#                     return redirect('Invoices:show_invoice', invoice.id)
#
#             if WarehouseTransactions.objects.filter(item=invoice_item.item, warehouse=warehouse.sub_warehouse):
#                 if invoice_item.main_unit_sub_warehouse > WarehouseTransactions.objects.filter(item=invoice_item.item, warehouse=warehouse.sub_warehouse).last().balance:
#                     invoice_item.delete()
#                     message = 'عفواً لاتوجد كمية كافية داخل المخزن الفرعي. الكمية المتاحة: ' + str(WarehouseTransactions.objects.filter(item=invoice_item.item, warehouse=warehouse.sub_warehouse).last().balance)
#                     messages.add_message(request, messages.ERROR, extra_tags='danger', message=message)
#                     return redirect('Invoices:show_invoice', invoice.id)
#
#     return redirect('Invoices:show_invoice', invoice.id)


def add_product_to_invoice2(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    form = InvoiceItemForm2(request.POST or None)

    if form.is_valid():
        prod = form.save(commit=False)
        form.instance.invoice = invoice
        prod.save()
        invoice_item = get_object_or_404(InvoiceItem, id=prod.id)
        invoice_item.calculate_main_units()

    return redirect('Invoices:show_invoice', invoice.id)