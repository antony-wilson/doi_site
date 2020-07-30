"""doi_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import re_path

from datasets.views import Mint
from doi_site.views import HomeView, DoiList, Domains, Notes, logout_view, login_user
from mds.views import MediaView, MetadataPost, DoiView, DoiDetail, MetadataView

urlpatterns = [
    re_path(r'^$', HomeView.as_view(), name='home'),
    re_path(r'^index$', HomeView.as_view(), name='index'),

    re_path(r'^admin/', admin.site.urls),

    # web
    re_path(r'^doilist$', DoiList.as_view(), name='doi_list'),
    re_path(r'^domains$', Domains.as_view(), name='domains'),
    re_path(r'^mint$', Mint.as_view(), name='mint'),
    re_path(r'^notes$', Notes.as_view(), name='notes'),

    # MDS
    re_path(r'^doi$', DoiView.as_view(), name='doi_view'),
    re_path(r'^doi/', DoiDetail.as_view(), name='doi_detail'),
    re_path(r'^metadata$', MetadataPost.as_view(), name='metadata_post'),
    re_path(r'^metadata/', MetadataView.as_view(), name='metadata_view'),
    re_path(r'^media/', MediaView.as_view(), name='media_view'),

    re_path(r'^accounts/login/$', login_user, name='login'),
    re_path(r'^logout/$', logout_view, name='logout'),

    re_path(r'', HomeView.as_view()),

]
