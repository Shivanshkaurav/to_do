from django.http import HttpResponseForbidden
from .throttles import *

class AdminLoginThrottleMiddleware:
       def __init__(self, get_response):
           self.get_response = get_response
           self.throttle = AdminLoginThrottle()

       def __call__(self, request):
           if not self.throttle.allow_request(request, None):
               return HttpResponseForbidden("Too many login attempts.")
           return self.get_response(request)