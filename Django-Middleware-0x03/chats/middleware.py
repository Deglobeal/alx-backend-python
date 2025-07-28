# chats/middleware.py

from datetime import datetime
from django.http import HttpResponseForbidden

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allow requests only between 9AM and 5PM
        current_hour = datetime.now().hour
        if current_hour < 9 or current_hour >= 17:
            return HttpResponseForbidden("Access not allowed at this time.")
        
        return self.get_response(request)
