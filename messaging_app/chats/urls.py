from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet
from rest_framework_nested.routers import NestedDefaultRouter

router = DefaultRouter()
router.register(r"conversations", ConversationViewSet, basename="conversations")
router.register(r"messages", MessageViewSet, basename="messages")

urlpatterns = [
    path("api/", include(router.urls)), 
]
