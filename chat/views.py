from django.views.generic import TemplateView, ListView
from django.views.generic.edit import BaseFormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.db.models import Q

from accounts.models import User
from chat.models import Chat, ChatRoom


class ChatView(TemplateView, BaseFormView):
    template_name = "chat/chatbox.html"
    form_class = None
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ChatView, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["user_id"] = self.request.user.id
        context_data["bot"] = User.ROLE_BOT
        context_data["profissional"] = User.ROLE_PROFESSIONAL
        context_data["patient"] = User.ROLE_PATIENT
        return context_data
    
    def get_form(self):
        return None
    
    def get(self, request, *args, **kwargs):
        chat_room = None
        me_chat_user = request.user
        you_chat_user = None
        if request.GET.get("user") and User.objects.filter(username=request.GET.get("user")).exists():
            you_chat_user = User.objects.get(username=request.GET.get("user"))
            
        if not you_chat_user and me_chat_user.role == User.ROLE_PATIENT and \
                not Chat.objects.filter(users__role=User.ROLE_PROFESSIONAL, users=me_chat_user).exists():
            return HttpResponseRedirect(reverse_lazy('add_chat'))

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
            you_chat_user = User.objects.filter(chats__users=me_chat_user).exclude(id=me_chat_user.id).distinct().first()
            chat_room = Chat.objects.filter(users=me_chat_user).filter(users=you_chat_user).first().chat_room
        
        kwargs["me_chat_user"] = me_chat_user
        kwargs["you_chat_user"] = you_chat_user
        kwargs["peoples_messages"] = chat_room.get_messages(request.user)
        kwargs["peoples"] = User.objects.filter(chats__users=me_chat_user).exclude(id=me_chat_user.id).distinct()
        kwargs["chat_room"] = chat_room
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_success_url(self, message=None):
        if message:
            messages.add_message(self.request, messages.INFO, 'Relação encerrada!')
        return reverse_lazy('chat')

    def post(self, request, *args, **kwargs):
        message = None
        if request.POST.get("chat_room_id"):
            if request.user.role == User.ROLE_BOT:
                message = _('Não é possível encerrar relação com o Bot!')
            else:
                chat_room = ChatRoom.objects.get(pk=int(request.POST.get("chat_room_id")))            
                chat_room.messages.all().delete()
                chat_room.chat.delete()
                chat_room.delete()
                message = _('Relação encerrada!')
        return HttpResponseRedirect(self.get_success_url(message=message))


class AddChatView(ListView):
    model = User
    template_name = "chat/add_chat.html"
    queryset = User.objects.filter(role=User.ROLE_PROFESSIONAL)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AddChatView, self).dispatch(*args, **kwargs)
    
    def get_queryset(self):
        queryset = User.objects.filter(role=User.ROLE_PROFESSIONAL)
        search = self.request.GET.get("q")
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) | Q(first_name__icontains=search) | Q(last_name__icontains=search)
            )
        return queryset
