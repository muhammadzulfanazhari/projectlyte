from django.contrib import admin
from django.urls import path
from projectlyte.appointment import views


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('appointment/', views.AppointmentAPI.as_view(), name='appointment'),
    path('health', views.HealthAPI.as_view(), name='health'),
    path('appointment/', views.AppointmentAPI.as_view(), name='appointment'),
]
