from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)

class LastSennAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'last_activity',)
    search_fields = ['user__username', ]
    list_filter = ['last_activity']

    def get_ordering(self, request):
        return ['last_activity']

admin.site.register(LastSeen, LastSennAdmin)
