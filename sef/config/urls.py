"""nugget URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve

from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework.documentation import include_docs_urls

from sef.user.views import MeView

apipatterns = ([
    path('user/', include('sef.user.urls')),
    path('facility/', include('sef.facility.urls')),
], 'v1')

authpatterns = [
    path('api-token-auth/', obtain_jwt_token, name='get-token'),
    path('api-token-refresh/', refresh_jwt_token, name='refresh-token'),
]

urlpatterns = [
    path('v1/', include(apipatterns)),
    path('', include('rest_framework.urls')),
    path('auth/', include(authpatterns)),
    path('me/', MeView.as_view(), name='me'),
    path('static/<path>/', serve, {'document_root': settings.STATIC_ROOT}), # noqa
    path('social/', include(('social_django.urls', 'social'))),
    path('docs/', include_docs_urls(
        title='Sef World', public=False)),
    # url(r'^media\/(?P<path>.*)$', serve_media, name='serve_media'),
]

if settings.DEBUG is True:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
