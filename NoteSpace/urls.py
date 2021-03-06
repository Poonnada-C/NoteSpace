"""NoteSpace URL Configuration

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
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from django.contrib import admin
from django.urls import include, path

from notes import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.home_page, name="home_page"),
    url(r'^upload/',views.upload_page, name='upload_page'),
    url(r'^api/upload/', views.upload_api, name='api_upload'),
    url(r'^api/addcomment/', views.add_comment_api, name='addcomment_api'),
    url(r'^notes/',include('notes.urls')),
    path("tag/<str:tag>", views.tag_query, name="tagQuery"),
    url(r'^search/$', views.search, name="search"),
    url(r'^about/', views.about, name='about'),
    path("help/", views.help, name='help'),
    path("help/<str:help_topic>", views.help_detail, name='help_detail'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
