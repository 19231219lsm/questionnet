"""back URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin

from django.urls import path
from django.views.generic import TemplateView

from myobject.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('', TemplateView.as_view(template_name="index.html")),
                  path('admin/', admin.site.urls),
                  path('register', register, name='register'),
                  path('login', login, name='login'),
                  path('createPDF', createPDF, name='createPDF'),
                  path('openquestion', openquestion, name='openquestion'),
                  path('edit', edit, name='edit'),
                  path('survey', survey, name='survey'),
                  path('manage', publish_or_delete, name='publish_or_delete'),
                  path('getIP', getIP, name='getIP'),
                  path('recycle', recycle_bin, name='recycle_bin'),
                  path('analysis', analysis, name='analysis'),
                  path('analysisForUser', analysisForUser, name='analysisForUser'),
                  path('getLocation', getLocation, name='getLocation'),
                  path('end3', end3, name='end3'),
                  path('printf', printf, name='printf')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
                  url(r'', TemplateView.as_view(template_name="index.html"))]
