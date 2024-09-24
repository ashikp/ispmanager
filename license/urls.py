from django.urls import path

from . import views

urlpatterns = [
    path('get_mac/', views.get_mac_ip_view),
    path('activate/', views.activate_license),
    path('good/', views.good),

]