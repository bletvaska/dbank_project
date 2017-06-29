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

urlpatterns = [

    url(r'^accounts/', include('accounts.urls')),

    # login/logout
    #url(r'^login/$', auth_views.login, name='login'),
    url(r'^login/$',
        auth_views.LoginView.as_view(redirect_authenticated_user=True),
        name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    # url(r'^$', HomepageView.as_view(), name='homepage'),

    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
