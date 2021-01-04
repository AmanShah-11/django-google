from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r'newevents', views.EventsView)

urlpatterns = [
    path('', views.schedule, name='schedule'),
    path('users', views.users, name='users'),
    path('events', views.events, name='events'),
    path('', include(router.urls))
]