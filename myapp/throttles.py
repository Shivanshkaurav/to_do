from rest_framework.throttling import UserRateThrottle , AnonRateThrottle

class AnonRateThrottles(AnonRateThrottle):
    scope = 'anna'

class SustainedRateThrottle(UserRateThrottle):
    scope = 'sustained'
    
class AdminLoginThrottle(UserRateThrottle):
    scope = 'admin_login'

    def allow_request(self, request, view):
        if request.path == '/admin/login/':
            return super().allow_request(request, view)
        return True