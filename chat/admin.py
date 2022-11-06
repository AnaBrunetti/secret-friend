from django.contrib import admin
from chat.models import (
    ChatRoom,
    Message,
    Chat,
)


@ admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ["slug"]
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = [
        [None, {
            "fields": ["slug"]
        }],
        ["Important dates", {
            "classes": ["collapse"],
            "fields": ["created_at", "updated_at"]
        }]
    ]
    search_fields = ["slug"]
    list_per_page = 12
    ordering = ["created_at"]


@ admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["user", "chat_room", "context"]
    readonly_fields = ["created_at", "updated_at"]
    autocomplete_fields = ["user", "chat_room"]
    fieldsets = [
        [None, {
            "fields": ["user", "chat_room", "context"]
        }],
        ["Important dates", {
            "classes": ["collapse"],
            "fields": ["created_at", "updated_at"]
        }]
    ]
    list_filter = ["user", "chat_room"]
    search_fields = ["user", "chat_room"]
    list_per_page = 12
    ordering = ["created_at"]


@ admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ["chat_room"]
    readonly_fields = ["created_at", "updated_at"]
    filter_horizontal = ["users"]
    fieldsets = [
        [None, {
            "fields": ["chat_room", "users"]
        }],
        ["Important dates", {
            "classes": ["collapse"],
            "fields": ["created_at", "updated_at"]
        }]
    ]
    search_fields = ["chat_room__slug"]
    list_per_page = 12
    ordering = ["created_at"]
