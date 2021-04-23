from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Branch)
admin.site.register(Warehouse)
admin.site.register(BranchWarehouses)