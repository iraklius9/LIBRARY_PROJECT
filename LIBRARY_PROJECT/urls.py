"""
URL configuration for LIBRARY project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from LIBRARY_PROJECT import settings
from books import views


urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('users/', include('users.urls')),
                  path('books/', include('books.urls', namespace='books')),
                  path('api/', include('api.urls')),
                  path('rest_framework/', include('rest_framework.urls')),
                  path('', views.library, name='library'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
