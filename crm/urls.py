from django.contrib import admin
from django.urls import path,include
from core.views import index,about,logout_view
from django.contrib.auth import views
from userprofile.forms import LoginForm


urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/',include('dashboard.urls')),
    path('dashboard/leads/',include('lead.urls')),
    path('dashboard/clients/',include('client.urls')),
    path('dashboard/',include('userprofile.urls')),
    path('dashboard/teams/',include('team.urls')),

    path('',index,name='index'),
    path('about/',about,name='about'),
    path('log-out/', logout_view, name='logout'),
    path('log-in/', views.LoginView.as_view(template_name='userprofile/login.html', authentication_form=LoginForm), name='login'),


    path('log-in/', views.LoginView.as_view(template_name='userprofile/login.html'), name='login'),


]
