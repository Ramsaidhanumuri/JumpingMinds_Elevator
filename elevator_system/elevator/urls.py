# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ElevatorViewSet, RequestViewSet

router = DefaultRouter()
router.register(r'elevators', ElevatorViewSet, basename='elevator')
router.register(r'requests', RequestViewSet, basename='request')

urlpatterns = [
    path('', include(router.urls)),
]
