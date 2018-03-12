from oauth2_provider.views.generic import ProtectedResourceView
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


class ApiEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return HttpResponse("hello!")


    def post(self, request, *args, **kwargs):
        return HttpResponse("hello post")


from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse


@login_required()
def secret_page(request, *args, **kwargs):
    return HttpResponse("secret", status=200)
