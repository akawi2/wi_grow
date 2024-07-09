from django.urls import path
from . import views

urlpatterns = [
    path('', views.getData),
    path('measurement/', views.create_environment_monitoring, name='measurement'),
    path('get_measurement/', views.get_environmental_monitoring, name='get_measurement'),
    path('incident/', views.get_incident, name='incident'),
    path('dashboard/', views.last_environmental_monitoring, name='dashboard'),
    path('discussion/', views.discussion, name='disussion'),
    path('predict/', views.predict_image, name='predict_image'),
]