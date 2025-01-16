"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from students import views
admin.site.site_title = "site admin"
admin.site.site_header = "Admin Page"
admin.site.index_title = "Administration"

from .views import *



urlpatterns = [
    path('' , views.index ),
    path('logout/', logout , name = 'logout'),
    path('test/', views.test, name='test'),
    path('guide/', views.guide, name='guide'),
    path('about_us/', views.about, name='about'),
    path('pagenotfount', views.pagenotfount, name='page_not_found'),
    path('admin_page', views.admin_page, name='admin_page'),
    # for admin
    path('admin/startattendance/', startattendance, name='startattendance'),
    path('admin/end_attendance/', end_attendance, name='end_attendance'),
    path('admin/dashboard/', dashboard, name='dashboard'),
    path('admin/add_student/', add_student, name='add_student'),
    path('admin/attendance/' , attendance , name='attendance'),
    path('admin/report_dashboard/', report_dashboard, name='report_dashboard'),
    path('admin/report/', report, name='report'),
    
    path('admin/', admin.site.urls, name='admin'),
    # Developer page
    path('developer_profile/', views.developer_profile, name='developer_profile'), 
    # path('accounts/', include('django.contrib.auth.urls')),
    path('student/accounts/', include('django.contrib.auth.urls')),
    path('student/', include('students.urls')),
   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


