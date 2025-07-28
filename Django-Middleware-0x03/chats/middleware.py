# chats/middleware.py

import time
import logging

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger('django.request')

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time
        method = request.method
        path = request.get_full_path()
        status = response.status_code

        log_message = f"{method} {path} {status} {duration:.2f}s"
        with open("requests.log", "a") as f:
            f.write(log_message + "\n")

        return response
