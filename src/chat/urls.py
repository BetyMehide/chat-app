from django.urls import path
from .views import ConversationListView, ConversationCreateView, MessageListView, ThoughtListView

app_name = "chat"
urlpatterns = [
    path("", ConversationListView.as_view(), name="conversations"),
    path("create_conversation/", ConversationCreateView.as_view(), name="create_conversation"),
    path("<int:id>/", MessageListView.as_view(), name="messages"),
    path("msg/<int:id>/", ThoughtListView.as_view(), name="thoughts"),
]
