#added throttling to implement rate limiting
from rest_framework.throttling import UserRateThrottle

class APIKeyRateThrottle(UserRateThrottle):
    scope = 'api_key'

    def get_cache_key(self, request, view):
        api_key = request.headers.get("Authorization")
        if api_key:
            return f'{self.scope}_{api_key}'
        return None
