from .views import *
from django.urls import path

app_name = 'Reports'
urlpatterns = [
    path('home/', ReportsHome.as_view(), name='ReportsHome'),
    path('invoice/', InvoiceReport.as_view(), name='InvoiceReport'),
    path('expense/', ExpenseReport.as_view(), name='ExpenseReport'),
    path('graph/expense/', ExpenseGraphReport.as_view(), name='ExpenseGraphReport'),
    path('graph/income/', IncomeGraphReport.as_view(), name='IncomeGraphReport'),
    path('treasury/balance/', TreasuryBalanceReport.as_view(), name='TreasuryBalanceReport'),
    path('treasury/transactions/', TreasuryTransactionReport.as_view(), name='TreasuryTransactionReport'),
    path('stock/item/balance/', item_stock_report, name='ItemStockReport'),
    path('stock/transactions/', item_transactions_report, name='item_transactions_report'),
    path('stock/branch/balance/', branch_stock_report, name='branch_stock_report'),
    path('stock/below_full_stock/', items_below_order_stock, name='items_below_order_stock'),
    path('stock/critical_stock/', items_below_critical_stock, name='items_below_critical_stock'),
    path('stock/not_sold/', not_sold_items_report, name='not_sold_items_report'),
    path('customer/statement/', CustomerStatementReport.as_view(), name='CustomerStatementReport'),
    path('customer/debitors/', DebitorsReport.as_view(), name='DebitorsReport'),
    path('customer/creditors/', CreditorsReport.as_view(), name='CreditorsReport'),
    path('accounts_reports/financial_list/', financial_list, name='financial_list'),
    path('accounts_reports/profit/', profit_loss, name='profit_loss'),
    path('maintenance_reports/maintenance_report/', maintenance_report, name='maintenance_report'),
    path('partner_reports/partner_percent/', partner_report_at, name='partner_report_at'),
    path('partner_reports/partner_transactions/', partner_transactions, name='partner_transactions'),
    path('graph/new_customers_report/', new_customers_report, name='new_customers_report'),
    path('graph/calls_report/', calls_report, name='calls_report'),
    path('graph/employee_report/', calls_report, name='employee_report'),

    #Ajax to return count and value for invoices
    path('api/invoice/', invoice_summary, name='invoice_summary'),
    path('api/invoice_summary_date/', invoice_summary_date, name='invoice_summary_date'),
    path('api/customer_sammery_date/',customer_sammery_date, name='customer_sammery_date'),
    
    path('api/debitors/', debitors_summery, name='debitors_summery'),
    path('api/craditors/', craditors_summery, name='craditors_summery'),
    path('api/customer_sammery/', customer_sammery, name='customer_sammery'),
    path('api/branch/' , branch , name='branch')
    ]