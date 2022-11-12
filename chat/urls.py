from django.urls import path

from chat.views import ChatView, AddChatView

urlpatterns = [
    path("", ChatView.as_view(), name="chat"),
    path("profissionais", AddChatView.as_view(), name="add_chat")
]
