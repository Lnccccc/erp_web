"""erp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from work_flow import views
from .views import verifed,homepage
from django.conf import settings
from django.views.static import serve
def i18n_javascript(request):
    return admin.site.i18n_javascript(request)
urlpatterns = [
    path('static/admin/jsi18n',i18n_javascript),
    path('index/',homepage),
    path('',views.IndexView.as_view(),name='index'),
    path('admin/jsi18n',i18n_javascript),
    path('admin/', include(admin.site.urls)),
    path('flow/',include('work_flow.urls',namespace='flow')),
    path('account/',include('account.urls',namespace='account')),
    path('MP_verify_YUe1siIcc5wabsNm.txt',verifed),
]
