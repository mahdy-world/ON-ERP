from .views import *
from django.urls import path

app_name = 'Products'
urlpatterns = [
    path('main_categories/', MainCategoryList.as_view(), name='MainCategoryList'),
    path('main_categories/new/', MainCategoryCreate.as_view(), name='MainCategoryCreate'),
    path('main_categories/trash/', MainCategoryTrashList.as_view(), name='MainCategoryTrashList'),
    path('main_categories/<int:pk>/edit/', MainCategoryUpdate.as_view(), name='MainCategoryUpdate'),
    path('main_categories/<int:pk>/delete/', MainCategoryDelete.as_view(), name='MainCategoryDelete'),
    
    path('sub_categories/', SubCategoryList.as_view(), name='SubCategoryList'),
    path('sub_categories/new/', SubCategoryCreate.as_view(), name='SubCategoryCreate'),
    path('sub_categories/trash/', SubCategoryTrashList.as_view(), name='SubCategoryTrashList'),
    path('sub_categories/<int:pk>/edit/', SubCategoryUpdate.as_view(), name='SubCategoryUpdate'),
    path('sub_categories/<int:pk>/delete/', SubCategoryDelete.as_view(), name='SubCategoryDelete'),

    path('manufactures/', ManufactureList.as_view(), name='ManufactureList'),
    path('manufactures/new/', ManufactureCreate.as_view(), name='ManufactureCreate'),
    path('manufactures/trash/', ManufactureTrashList.as_view(), name='ManufactureTrashList'),
    path('manufactures/<int:pk>/edit/', ManufactureUpdate.as_view(), name='ManufactureUpdate'),
    path('manufactures/<int:pk>/delete/', ManufactureDelete.as_view(), name='ManufactureDelete'),

    path('brands/', BrandList.as_view(), name='BrandList'),
    path('brands/new/', BrandCreate.as_view(), name='BrandCreate'),
    path('brands/trash/', BrandTrashList.as_view(), name='BrandTrashList'),
    path('brands/<int:pk>/edit/', BrandUpdate.as_view(), name='BrandUpdate'),
    path('brands/<int:pk>/delete/', BrandDelete.as_view(), name='BrandDelete'),

    path('units/', UnitList.as_view(), name='UnitList'),
    path('units/new/', UnitCreate.as_view(), name='UnitCreate'),
    path('units/trash/', UnitTrashList.as_view(), name='UnitTrashList'),
    path('units/<int:pk>/edit/', UnitUpdate.as_view(), name='UnitUpdate'),
    path('units/<int:pk>/delete/', UnitDelete.as_view(), name='UnitDelete'),

    path('products/', ProductList.as_view(), name='ProductList'),
    path('products/new/', ProductCreate.as_view(), name='ProductCreate'),
    path('products/add/', product_create, name='product_create'),
    path('products/trash/', ProductTrashList.as_view(), name='ProductTrashList'),
    path('products/<int:pk>/edit/', ProductUpdate.as_view(), name='ProductUpdate'),
    path('products/<int:pk>/delete/', ProductDelete.as_view(), name='ProductDelete'),
    path('products/<int:pk>/show/', ProductCard.as_view(), name='ProductCard'),
    path('products/<int:pk>/add_content/', GroupedProductCreate.as_view(), name='GroupedProductCreate'),
    path('products/<int:pk>/note_update/', ProductNoteUpdate.as_view(), name='ProductNoteUpdate'),

    path('grouped_product/<int:pk>/<int:ppk>/edit/', GroupedProductUpdate.as_view(), name='GroupedProductUpdate'),
    path('grouped_product/<int:pk>/<int:ppk>/delete/', GroupedProductDelete.as_view(), name='GroupedProductDelete'),

    #########################################

    path('prices/<int:pk>/add_content/', PricesProductCreate.as_view(), name='PricesProductCreate'),
    path('prices_product/<int:pk>/<int:ppk>/edit/', PricesProductUpdate.as_view(), name='PricesProductUpdate'),
    path('prices_product/<int:pk>/<int:ppk>/delete/', PricesProductDelete.as_view(), name='PricesProductDelete'),
    path('prices_product/<int:pk>/stop/', PricesProductStop.as_view(), name='PricesProductStop'),
    path('prices_product/<int:pk>/active/', PricesProductActive.as_view(), name='PricesProductActive'),
    path('prices_product/editAll/', PricesProductEditAll, name='PricesProductEditAll'),
    path('products/<int:pk>/editPrice/', ProductPriceUpdate.as_view(), name='ProductPriceUpdate'),

    path('main_prices/', MainPricesList.as_view(), name='MainPricesList'),
    path('main_prices/new/', MainPricesListCreate.as_view(), name='MainPricesListCreate'),
    path('main_prices/trash/', MainPricesTrashList.as_view(), name='MainPricesTrashList'),
    path('main_prices/<int:pk>/edit/', MainPricesListUpdate.as_view(), name='MainPricesListUpdate'),
    path('main_prices/<int:pk>/delete/', MainPricesListDelete.as_view(), name='MainPricesListDelete'),
    path('main_prices/<int:pk>/show/', PricesListCard.as_view(), name='PricesListCard'),
    path('prices_product_list/editAll/', PricesProductListEditAll, name='PricesProductListEditAll'),

    path('product_units/<int:pk>/add_unit/', ProductUnitCreate.as_view(), name='ProductUnitCreate'),
    path('product_units/<int:pk>/edit/', ProductUnitUpdate.as_view(), name='ProductUnitUpdate'),
    path('product_units/<int:pk>/delete/', ProductUnitDelete.as_view(), name='ProductUnitDelete'),


    path('customerprices/<int:pk>/<int:ppk>/edit/', CustomerPricesUpdate.as_view(), name='CustomerPricesUpdate'),
    path('customerprices/<int:pk>/<int:ppk>/delete/', CustomerPricesDelete.as_view(), name='CustomerPricesDelete'),

]
