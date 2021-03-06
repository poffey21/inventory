"""www URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from scanner.views import ReceiptCreateView
from scanner.views import ReceiptUploadView
from scanner.views import ReceiptUpdateView
from scanner.views import ExampleFormView

urlpatterns = [
    url(r'^$', ReceiptUploadView.as_view()),
    url(r'^receipt/(?P<pk>\d+)/$', ReceiptUpdateView.as_view(), name='update-receipt'),
    url(r'^upload/$', ExampleFormView.as_view()),
    url(r'^form/$', ReceiptCreateView.as_view()),
    url(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
