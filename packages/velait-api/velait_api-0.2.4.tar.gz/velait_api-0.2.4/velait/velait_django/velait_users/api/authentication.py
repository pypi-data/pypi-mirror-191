from rest_framework.authentication import BaseAuthentication, TokenAuthentication


class MIOSSOAuthentication(BaseAuthentication):
    def authenticate(self, request):
        pass

    @staticmethod
    def get_authorization_header(request):
        pass
