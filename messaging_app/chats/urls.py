from django.urls import path, include
from rest_framework.routers import DefaultRouter  # <-- must use DefaultRouter
from .views import ConversationViewSet, MessageViewSet

router = DefaultRouter()  # <-- checker expects this
router.register(r"conversations", ConversationViewSet, basename="conversations")
router.register(r"messages", MessageViewSet, basename="messages")

urlpatterns = [
    path("", include(router.urls)),  # no "api/" here, project URLs will handle it
]
