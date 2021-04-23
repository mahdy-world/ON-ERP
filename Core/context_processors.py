from Auth.models import User
from Products.models import *
from Customers.models import *
from Branches.models import *
from Invoices.models import *
from Notifications.models import Notification
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import *
from datetime import datetime ,timedelta
from django.db.models import Q
from Reports.views import *
from django.http import request




def allcontext(request):
    
    # Return offline user
    def off_users():
        offline_user =LastSeen.get_user_offline(timedelta(seconds=180)).exclude(user=request.user.id) # to exclude instanc user
        return offline_user

 
    # Return online user 
    def on_users():
        online_user =LastSeen.get_user_active(timedelta(seconds=180)).exclude(user=request.user.id) # to exclude instanc user
        return online_user

    def All_branches():
        queryset = Branch.objects.all()
        return queryset
        
    return {
        'off' :off_users(),
        'on' : on_users(),
        'all_branches' :All_branches() 
    }

