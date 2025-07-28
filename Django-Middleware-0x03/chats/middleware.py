# chats/middleware.py

from datetime import datetime
from django.http import HttpResponseForbidden
import time
from django.http import JsonResponse

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


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Store timestamps of messages per IP
        self.ip_message_times = {}

    def __call__(self, request):
        if request.method == "POST" and request.path.startswith("/chat/"):  # Adjust path as needed
            ip = self.get_client_ip(request)
            current_time = time.time()
            window = 60  # seconds (1 minute)
            limit = 5    # max messages per window

            if ip not in self.ip_message_times:
                self.ip_message_times[ip] = []

            # Remove timestamps outside the time window
            self.ip_message_times[ip] = [t for t in self.ip_message_times[ip] if current_time - t < window]

            if len(self.ip_message_times[ip]) >= limit:
                return JsonResponse(
                    {"error": "Message limit exceeded. Please wait before sending more messages."},
                    status=429,
                )

            # Log this message timestamp
            self.ip_message_times[ip].append(current_time)

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Get client IP address from request headers."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Apply only to restricted endpoints. Adjust path or methods as needed.
        restricted_paths = ["/chat/delete/", "/chat/admin/"]  # example protected routes
        if request.path in restricted_paths:
            if not request.user.is_authenticated:
                return JsonResponse({"error": "Authentication required"}, status=403)

            # Assuming user role is stored in request.user.role or user.profile.role
            # Replace this logic based on your model setup
            user_role = getattr(request.user, 'role', None)

            if user_role not in ["admin", "moderator"]:
                return JsonResponse({"error": "Forbidden: insufficient permissions"}, status=403)

        return self.get_response(request)
