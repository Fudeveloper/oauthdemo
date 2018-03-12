# """oauthdemo URL Configuration
#
# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/2.0/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
# from django.contrib import admin
# from django.urls import path
# # from django.conf.urls import url, include
# #
# # urlpatterns = [
# #     path('admin/', admin.site.urls),
# #     url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
# # ]
#
# from django.conf.urls import url, include
# import oauth2_provider.views as oauth2_views
# from django.conf import settings
# from .views import ApiEndpoint
# from . import views
# # OAuth2 provider endpoints
# oauth2_endpoint_views = [
#     url(r'^authorize/$', oauth2_views.AuthorizationView.as_view(), name="authorize"),
#     url(r'^token/$', oauth2_views.TokenView.as_view(), name="token"),
#     url(r'^revoke-token/$', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
# ]
#
# if settings.DEBUG:
#     # OAuth2 Application Management endpoints
#     oauth2_endpoint_views += [
#         url(r'^applications/$', oauth2_views.ApplicationList.as_view(), name="list"),
#         url(r'^applications/register/$', oauth2_views.ApplicationRegistration.as_view(), name="register"),
#         url(r'^applications/(?P<pk>\d+)/$', oauth2_views.ApplicationDetail.as_view(), name="detail"),
#         url(r'^applications/(?P<pk>\d+)/delete/$', oauth2_views.ApplicationDelete.as_view(), name="delete"),
#         url(r'^applications/(?P<pk>\d+)/update/$', oauth2_views.ApplicationUpdate.as_view(), name="update"),
#     ]
#
#     # OAuth2 Token Management endpoints
#     oauth2_endpoint_views += [
#         url(r'^authorized-tokens/$', oauth2_views.AuthorizedTokensListView.as_view(), name="authorized-token-list"),
#         url(r'^authorized-tokens/(?P<pk>\d+)/delete/$', oauth2_views.AuthorizedTokenDeleteView.as_view(),
#             name="authorized-token-delete"),
#     ]
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     # OAuth 2 endpoints:
#     url(r'^o/', include(oauth2_endpoint_views)),
#     url(r'^api/hello', ApiEndpoint.as_view()),  # an example resource endpoint
#     url(r'^secret/$', views.secret_page, name='secret'),
# ]



from django.conf.urls import url, include
from django.contrib.auth.models import User, Group
from django.contrib import admin

admin.autodiscover()

from rest_framework import permissions, routers, serializers, viewsets

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope


# first we define the serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


# Routers provide an easy way of automatically determining the URL conf
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.

from django.urls import path
from . import views
import oauth2_provider.views as oauth2_views
from django.conf import settings


oauth2_endpoint_views = [
    url(r'^authorize/$', oauth2_views.AuthorizationView.as_view(), name="authorize"),
    url(r'^token/$', oauth2_views.TokenView.as_view(), name="token"),
    url(r'^revoke-token/$', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
]

if settings.DEBUG:
    # OAuth2 Application Management endpoints
    oauth2_endpoint_views += [
        url(r'^applications/$', oauth2_views.ApplicationList.as_view(), name="list"),
        url(r'^applications/register/$', oauth2_views.ApplicationRegistration.as_view(), name="register"),
        url(r'^applications/(?P<pk>\d+)/$', oauth2_views.ApplicationDetail.as_view(), name="detail"),
        url(r'^applications/(?P<pk>\d+)/delete/$', oauth2_views.ApplicationDelete.as_view(), name="delete"),
        url(r'^applications/(?P<pk>\d+)/update/$', oauth2_views.ApplicationUpdate.as_view(), name="update"),
    ]

    # OAuth2 Token Management endpoints
    oauth2_endpoint_views += [
        url(r'^authorized-tokens/$', oauth2_views.AuthorizedTokensListView.as_view(), name="authorized-token-list"),
        url(r'^authorized-tokens/(?P<pk>\d+)/delete/$', oauth2_views.AuthorizedTokenDeleteView.as_view(),
            name="authorized-token-delete"),
    ]


urlpatterns = [
    url(r'^api/hello', views.ApiEndpoint.as_view()),
    path('admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^secret/$', views.secret_page, name='secret'),
    # ...
]