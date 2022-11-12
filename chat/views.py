from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from accounts.models import User
from chat.models import Chat, ChatRoom, Message


class ChatView(TemplateView):
    template_name = "chat/chatbox.html"
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ChatView, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["user_id"] = self.request.user.id
        return context_data
    
    def get(self, request, *args, **kwargs):
        chat_room = None
        me_chat_user = request.user
        you_chat_user = None
        if request.GET.get("user") and User.objects.filter(username=request.GET.get("user")).exists():
            you_chat_user = User.objects.get(username=request.GET.get("user"))

        if you_chat_user and Chat.objects.filter(users=me_chat_user).filter(users=you_chat_user).exists():
            chat_room = Chat.objects.filter(users=me_chat_user).filter(users=you_chat_user).first().chat_room
        elif you_chat_user and not Chat.objects.filter(users=me_chat_user).filter(users=you_chat_user).exists():
            slug = f"{me_chat_user.username}-{you_chat_user.username}"
            chat_room = ChatRoom.objects.create(
                slug=slug
            )
            chat = Chat.objects.create(
                chat_room=chat_room
            )
            chat.users.add(me_chat_user)
            chat.users.add(you_chat_user)
        elif not you_chat_user and Chat.objects.filter(users=me_chat_user).exists():
            chat = Chat.objects.filter(users=me_chat_user).first()
            chat_room = chat.chat_room
            you_chat_user = chat.users.exclude(id=me_chat_user.id).first()
        else:
            return HttpResponseRedirect(reverse_lazy('add_chat'))
        
        kwargs["me_chat_user"] = me_chat_user
        kwargs["you_chat_user"] = you_chat_user
        kwargs["messages"] = chat_room.get_messages(request.user)
        kwargs["peoples"] = User.objects.filter(chats__users=me_chat_user).exclude(id=me_chat_user.id).distinct()
        kwargs["chat_room"] = chat_room
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class AddChatView(TemplateView):
    template_name = "chat/add_chat.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AddChatView, self).dispatch(*args, **kwargs)