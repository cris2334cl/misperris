"""
URL configuration for MisPerrisProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
from django.urls import path

from MisPerrisApp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('mascotas/', views.mascotas, name='mascotas'),
    path('mascotas/crear/', views.mascota_crear, name='mascota_crear'),
    path('mascotas/editar/<int:pk>/', views.mascota_editar, name='mascota_editar'),
    path('mascotas/eliminar/<int:pk>/', views.mascota_eliminar, name='mascota_eliminar'),
    path('admin/', admin.site.urls),
]
