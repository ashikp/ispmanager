from rest_framework.authentication import TokenAuthentication

class BearerTokenAuthentication(TokenAuthentication):
    keyword = 'Bearer'  # Override the keyword to 'Bearer'
