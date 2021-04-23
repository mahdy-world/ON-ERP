import datetime

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from .models import LastSeen , User
from django.utils import timezone




# class UpdateLastActivityMiddleware(MiddlewareMixin):
#     # @staticmethod
#     # def process_request( request):
    #     user=request.user
    #     if  user__id.is_authenticated:
    #        return none
    #     LastSeen.update_user(user__id)    

    # @staticmethod    
    # def process_view(request) :
    #     assert hasattr(request, 'user'), 'The UpdateLastActivityMiddleware requires authentication middleware to be installed.'
    #     if not request.user.is_authenticated:
    #         Lastseen.objects.filter(user__id=request.user.id) \
    #                        .update_or_create( defaults={'last_activity':timezone.now()})

    # LastSeen.objects.update_or_create(user__id=user.id , defaults={'last_activity':timezone.now()})    

class UpdateLastActivityMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response
    
       
        
    def __call__(self, request):
        if request.user.is_authenticated:
            # Update last visit time after request finished processing.
            # user = User.objects.get(id=request.user.id)
            # print(user)
            last = LastSeen.objects.filter(user_id=request.user.id).first()
            print(last)
            if last:
                last.last_activity=timezone.now()
                last.save()
            else:
                LastSeen.objects.create(user_id=request.user.id, last_activity=timezone.now())

        response = self.get_response(request)
        

        return response


# class LastVisitMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if request.user.is_authenticated:
#             # Update last visit time after request finished processing.
#             user = User.objects.get(id=request.user.id)
#             userLastVisit = UserLastVisit.objects.filter(user_id=user)
#             if userLastVisit:
#                 userLastVisit.update(last_visit=now())
#             else:
#                 UserLastVisit.objects.create(user_id=user, last_visit=now())

#         response = self.get_response(request)
#         return response