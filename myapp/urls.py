from django.urls import path

from . import views

urlpatterns = [
    path('', views.schedule, name='schedule'),
    path('users', views.users, name='users'),
    path('events', views.events, name='events'),
]