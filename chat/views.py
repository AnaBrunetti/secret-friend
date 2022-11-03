from django.shortcuts import render

def chat_box(request, chat_box_name):
    return render(request, "chat/chatbox.html", {"chat_box_name": chat_box_name})