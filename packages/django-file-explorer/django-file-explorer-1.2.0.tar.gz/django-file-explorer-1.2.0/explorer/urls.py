from django.urls import path

from . import views
from .admin import explorer_admin

urlpatterns = [
    path('admin/', explorer_admin.urls),
    path('about', views.About.as_view(), name='explorer-about'),
    path('login/', views.Login.as_view(), name='explorer-login'),
    path('logout/', views.Logout.as_view(), name='explorer-logout'),
    path('', views.Explorer.as_view(), name='explorer-main'),

]
