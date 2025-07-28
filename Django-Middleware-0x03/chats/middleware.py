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
    
# chats/middleware.py

import time

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        response = self.get_response(request)

        end_time = time.time()
        duration = end_time - start_time

        method = request.method
        path = request.get_full_path()
        status_code = response.status_code

        log_message = f"{method} {path} {status_code} {duration:.2f}s\n"

        with open("requests.log", "a") as log_file:
            log_file.write(log_message)

        return response

