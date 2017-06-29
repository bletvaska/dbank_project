"""dbank URL Configuration

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
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

# from accounts.views import HomepageView
from django.views.generic import TemplateView
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='dBank REST API')

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # login/logout
    url(r'^login/$',
        auth_views.LoginView.as_view(redirect_authenticated_user=True),
        name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^$', TemplateView.as_view(template_name='homepage.html'), name='homepage'),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^transactions/', include('transactions.urls', namespace='transactions')),
    url(r'^clients/', include('clients.urls', namespace='clients')),

    url(r'^docs/$', schema_view),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
