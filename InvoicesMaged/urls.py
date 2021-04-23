from django.urls import path

from .views import *

app_name = 'InvoicesMaged'
urlpatterns = [
    path('search/', search_invoice, name='search_invoice'),
    path('setting/print/', invoice_setting, name='invoice_setting'),
    path('setting/base/', invoice_base_setting, name='invoice_base_setting'),
    path('expense/', expense_invoice, name='expense_invoice'),
    path('edit/<int:pk>/fast/', edit_fast_invoice, name='edit_fast_invoice'),
    path('income/', income_invoice, name='income_invoice'),
    path('capital/outcome/', capital_minus, name='capital_minus'),
    path('treasury/transfer/add/', treasury_transfer, name='treasury_transfer'),
    path('capital/income/', capital_plus, name='capital_plus'),
    # path('customer/outcome/', customer_outcome, name='customer_outcome'),
    # path('customer/income/', customer_income, name='customer_income'),
    path('new/<int:type>/', make_invoice, name='make_invoice'),
    path('show/<int:pk>/', show_invoice, name='show_invoice'),
    path('print/<int:pk>/', print_invoice, name='print_invoice'),
    path('last/<int:type>/', get_last_invoice, name='get_last_invoice'),
    path('save/<int:pk>/', save_invoice, name='save_invoice'),
    path('add_customer/<int:pk>/', add_customer_to_invoice, name='add_customer_to_invoice'),
    path('unsave/<int:pk>/', unsave_invoice, name='unsave_invoice'),
    path('delete/<int:pk>/', delete_invoice, name='delete_invoice'),
    path('super_delete/<int:pk>/', super_delete, name='super_delete'),
    path('opened/<int:type>/', show_opened_invoices, name='show_opened_invoices'),
    path('edit/discount/<int:pk>/', edit_invoice_discount, name='edit_invoice_discount'),
    path('edit/customer/<int:pk>/', edit_invoice_customer, name='edit_invoice_customer'),
    path('edit/branch/<int:pk>/', edit_invoice_branch, name='edit_invoice_branch'),
    path('edit/treasury/<int:pk>/', edit_invoice_treasury, name='edit_invoice_treasury'),
    path('edit/date/<int:pk>/', edit_invoice_date, name='edit_invoice_date'),
    path('items/delete/<int:pk>/', delete_invoice_item, name='delete_invoice_item'),
    path('items/edit/price/<int:pk>/', edit_invoice_item_price, name='edit_invoice_item_price'),
    path('items/edit/quantity/<int:pk>/', edit_invoice_item_quantity, name='edit_invoice_item_quantity'),
    path('items/edit/discount/<int:pk>/', edit_invoice_item_discount, name='edit_invoice_item_discount'),
    path('<int:invoice_id>/get_unit_price/', get_unit_price, name='get_unit_price'),
    # path('spend_categories/', SpendCategoryList.as_view(), name='SpendCategoryList'),
    # path('spend_categories/new/', SpendCategoryCreate.as_view(), name='SpendCategoryCreate'),
    # path('spend_categories/trash/', SpendCategoryTrashList.as_view(), name='SpendCategoryTrashList'),
    # path('spend_categories/<int:pk>/edit/', SpendCategoryUpdate.as_view(), name='SpendCategoryUpdate'),
    # path('spend_categories/<int:pk>/delete/', SpendCategoryDelete.as_view(), name='SpendCategoryDelete'),

    ##############################################################

    path('add_product/<int:pk>/', add_product_to_invoice, name='add_product_to_invoice'),
    path('<int:invoice_id>/get_unit_all_price/', get_unit_all_price, name='get_unit_all_price'),
    path('get_product_units/', get_product_units, name='get_product_units'),
    path('items/edit/main_warehouse/<int:pk>/', edit_invoice_item_main_warehouse, name='edit_invoice_item_main_warehouse'),
    path('items/edit/sub_warehouse/<int:pk>/', edit_invoice_item_sub_warehouse, name='edit_invoice_item_sub_warehouse'),
    path('pay/<int:pk>/', pay_invoice, name='pay_invoice'),
    path('out/<int:pk>/', out_invoice, name='out_invoice'),

]
