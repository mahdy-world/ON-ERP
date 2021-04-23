from django.db import models


# Create your models here.
class Tag(models.Model):
    word = models.CharField(max_length=35)
    slug = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return self.word


class HomePageSlider(models.Model):
    image = models.ImageField(verbose_name='الصورة')
    title = models.CharField(max_length=128, verbose_name='العنوان', null=True, blank=True)
    description = models.TextField(verbose_name='تعليق', null=True, blank=True)
    url = models.URLField(verbose_name='تحويل إلي', null=True, blank=True)
    disabled = models.BooleanField(default=False, verbose_name='تعطيل')

    def __str__(self):
        return str(self.id)


class Page(models.Model):
    title = models.CharField(max_length=128, verbose_name='اسم الصفحة')
    content = models.TextField(verbose_name='محتوي الصفحة')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='الكلمات الدلالية')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='تحت صفحة')
    add_to_menu = models.BooleanField(default=False, verbose_name='إضافة للقائمة الرئيسية')

    def __str__(self):
        return self.title


class WebsiteSetting(models.Model):
    primary_color = models.CharField(null=True, blank=True, default='#000000', verbose_name='اللون الاساسي',
                                     max_length=7)
    primary_text_color = models.CharField(null=True, blank=True, default='#ffffff',
                                          verbose_name='لون النص في اللون الاساسي', max_length=7)
    title = models.CharField(max_length=128, default='ON-Link', verbose_name="اسم الموقع")
    logo = models.ImageField(null=True, blank=True, verbose_name='الشعار')

    def __str__(self):
        return self.title
