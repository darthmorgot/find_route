"""travel URL Configuration

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
from django.contrib import admin
from django.urls import path, include

from routes.views import home, find_routes, add_route, save_route, RouteListView, RouteDetailView, RouteDeleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('cities/', include('cities.urls', namespace='cities')),
    path('trains/', include('trains.urls', namespace='trains')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('find_routes/', find_routes, name='find_routes'),
    path('add_route/', add_route, name='add_route'),
    path('save_route/', save_route, name='save_route'),
    path('list_route/', RouteListView.as_view(), name='list_route'),
    path('detail_route/<int:pk>/', RouteDetailView.as_view(), name='detail_route'),
    path('delete_route/<int:pk>/', RouteDeleteView.as_view(), name='delete_route'),
]
