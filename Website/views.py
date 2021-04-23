from django.urls import reverse_lazy
from django.urls import reverse_lazy
from django.views.generic import *
from Invoices.models import *
from .forms import *
from django.db.models import Q


# Create your views here.
class HomePage(TemplateView):
    template_name = 'Website/homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        setting = WebsiteSetting.objects.get_or_create(id=1)
        setting = WebsiteSetting.objects.get(id=1)
        context['setting'] = setting
        homepage_slider = HomePageSlider.objects.all()
        context['slides'] = homepage_slider
        context['navbar_pages'] = Page.objects.filter(add_to_menu=True)
        context['main_categories'] = MainCategory.objects.filter(deleted=False)
        return context


class Shop(TemplateView):
    template_name = 'Website/shop.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        setting = WebsiteSetting.objects.get_or_create(id=1)
        setting = WebsiteSetting.objects.get(id=1)
        context['setting'] = setting
        context['main_categories'] = MainCategory.objects.filter(deleted=False)
        return context


class ProductView(DetailView):
    model = Product
    template_name = 'Website/ProductView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        setting = WebsiteSetting.objects.get_or_create(id=1)
        setting = WebsiteSetting.objects.get(id=1)
        context['setting'] = setting
        context['main_categories'] = MainCategory.objects.filter(deleted=False)
        return context


class ProductList(ListView):
    model = Product
    template_name = 'Website/productList.html'
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        setting = WebsiteSetting.objects.get_or_create(id=1)
        setting = WebsiteSetting.objects.get(id=1)
        context['setting'] = setting
        context['main_categories'] = MainCategory.objects.filter(deleted=False)
        return context

    def get_queryset(self):
        queryset = Product.objects.filter(deleted=False)
        sub_category_id = self.kwargs['pk']
        queryset = queryset.filter(sub_category__id=sub_category_id)
        return queryset


class Search(ProductList):
    def get_queryset(self):
        queryset = Product.objects.filter(deleted=False)
        if self.request.GET.get('q'):
            s = self.request.GET.get('q')
            queryset = queryset.filter(
                Q(name__icontains=s) |
                Q(description__icontains=s) |
                Q(brand__name__icontains=s) |
                Q(manufacture__name__icontains=s) |
                Q(sub_category__name__icontains=s) |
                Q(sub_category__main_category__name__icontains=s)
            )
        if self.request.GET.get('sub_category'):
            queryset = queryset.filter(sub_category__id=self.request.GET.get('sub_category'))
        if self.request.GET.get('main_category'):
            queryset = queryset.filter(sub_category__main_category__id=self.request.GET.get('main_category'))
        if self.request.GET.get('brand'):
            queryset = queryset.filter(brand__id=self.request.GET.get('brand'))
        return queryset


def get_user_invoice(request):
    if request.user.invoice_set.filter(saved=False).count > 0:
        opened_invoice = request.user.invoice_set.filter(saved=False)[0]
    else:
        opened_invoice = Invoice()
        opened_invoice.creator = request.user
        opened_invoice.invoice_type = 3
        opened_invoice.save()
    return opened_invoice


class AddToCart(CreateView):
    model = InvoiceItem
    template_name = 'Website/form.html'
    form_class = AddToCartForm
    success_url = reverse_lazy('Website:Shop')

    def form_valid(self, form):
        product = Product.objects.get(id=self.request.GET.get('product'))
        invoice = get_user_invoice(self.request)
        item = form.save(commit=False)
        item.invoice = invoice
        item.product = product
        item.unit_price = product.sell_price
        item.total_price = item.unit_price * item.quantity
        item.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Product.objects.get(id=self.request.GET.get('product'))
        context['title'] = 'إضافة' + str(product.name) + 'إلي سلة الشراء'
        setting = WebsiteSetting.objects.get_or_create(id=1)
        setting = WebsiteSetting.objects.get(id=1)
        context['setting'] = setting
        context['main_categories'] = MainCategory.objects.filter(deleted=False)
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class MyOrders(ListView):
    model = Invoice
    template_name = 'Website/my_orders.html'
    paginate_by = 30

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        setting = WebsiteSetting.objects.get_or_create(id=1)
        setting = WebsiteSetting.objects.get(id=1)
        context['setting'] = setting
        context['main_categories'] = MainCategory.objects.filter(deleted=False)
        return context

    def get_queryset(self):
        queryset = Invoice.objects.filter(creator=self.request.user, invoice_type=3)
        return queryset


class MyCart(TemplateView):
    template_name = 'Website/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        setting = WebsiteSetting.objects.get_or_create(id=1)
        setting = WebsiteSetting.objects.get(id=1)
        context['setting'] = setting
        context['main_categories'] = MainCategory.objects.filter(deleted=False)
        context['object'] = get_user_invoice(self.request)
        return context
