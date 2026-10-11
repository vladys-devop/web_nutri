from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path
from clientes.views import inicio

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('',inicio, name='inicio'),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    ]
