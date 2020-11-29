"""museum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from main import views as mv



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',mv.ShowMP,name='main'),
    path('news/<int:new_id>',mv.ShowNewPage,name='new'),
    path('directions/<int:dir_id>',mv.ShowDirections,name='directions'),
    path('exhibition/<int:ex_id>',mv.ShowExhibition,name='exh'),
    path('exhibit/<int:exh_id>',mv.ShowExhibit,name='exhibit'),
    path('ajaxnewinfo/',mv.ShowNewInfoAjax,name='ajaxnewinfo'),
    path('feedback/',mv.ShowFeedB,name='fb'),
    path('sfeedback/',mv.ShowSuccessFeedback,name='success_feedback'),
    path('captcha/', include('captcha.urls')),
    path('administration/',mv.ShowAdminContacts,name='administration'),
    path('getbio/',mv.SendEmpBio,name='Biochanger'),
    path('exhibitinfo/',mv.SendExhibitInfo,name='exhibitinfo'),
    path('search/', mv.SearchView.as_view(), name='search'),
    path('contact/',mv.ShowContact,name='contact'),



]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
   import debug_toolbar
   urlpatterns = [
   path('__debug__/', include(debug_toolbar.urls)),]+urlpatterns
