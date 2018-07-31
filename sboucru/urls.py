"""sboucru URL Configuration

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
from django.contrib.auth import views as auth_views
from django.urls import path, include, reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500


from . import views
from sboapp.forms import CustomAuthForm

urlpatterns = [
        #Registration
    path('', auth_views.login, kwargs={'template_name': 'pages/home.html', 'authentication_form':CustomAuthForm}, name='login'),
    path('logout/', auth_views.logout, {'next_page': '/'}, name='logout'),
    path('sboapp/', include('sboapp.urls', namespace="sboapp")),
    path('admin/', admin.site.urls),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


handler404 = 'sboapp.views.error_404_view'
#handler500 = 'sboapp.views.error_500_view'
