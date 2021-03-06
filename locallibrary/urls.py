"""locallibrary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
#Use include() to add paths from the catalog application
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalog/', include('catalog.urls')),
    #将带有catalog/的请求转发到模块catalog.urls（使用相对路径URL/catalog/urls.py)就是从更目录向下找
]
#Add URL maps to redirect the base URL to our application from django.views.generic import RedirectView

urlpatterns +=[
    path('', RedirectView.as_view(url='/catalog')),
    path('accounts/', include('django.contrib.auth.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_toot=settings.STATIC_ROOT)
