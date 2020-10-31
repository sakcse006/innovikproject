"""copyproject URL Configuration

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

# from django.contrib import admin
# from django.conf.urls import url, include
# urlpatterns = [
#     url(r'^admin/', admin.site.urls),
#     url(r'^folder/', include('folder.urls') ,name='folder'), 
# ]
from django.contrib import admin
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from folder import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', views.index,name='index'),
    url(r'^get_subject_by_standard', views.get_subject_by_standard, name='get_subject_by_standard'),
    url(r'^get_subject', views.get_subject, name='get_subject'),
    url(r'^get_standard', views.get_standard, name='get_standard'),
    url(r'^get_standard_name', views.get_standard_name, name='get_standard_name'),
    url(r'^get_faculty', views.get_faculty, name='get_faculty'),
    url(r'^create_school_db', views.create_school_db, name='create_school_db'),
    url(r'^setup_apps_list', views.setup_apps_list, name='setup_apps_list'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
