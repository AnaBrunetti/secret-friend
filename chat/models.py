from django.db import models
from django.utils.translation import ugettext_lazy as _

from accounts.models import User
from helpers.models import TimestampModel

class ChatRoom(TimestampModel):
    slug = models.SlugField(
        verbose_name=_("Slug"),
        max_length=255,
        unique=True
    )

    class Meta:
        verbose_name = _("Sala de Conversa")
        verbose_name_plural = _("Salas de Conversa")
        
    def __str__(self):
        return self.slug

    def get_messages(self, user):
        messages = []
        for message in self.messages.all():
            messages.append({
                "type": "me" if user == message.user else "you",
                "context": message.context
            })
        return messages if messages != [] else None


class Message(TimestampModel):
    user = models.ForeignKey(
        verbose_name=_("Usuário"),
        to=User,
        related_name=_("messages"),
        on_delete=models.CASCADE
    )
    chat_room = models.ForeignKey(
        verbose_name=_("Sala de Conversa"),
        to=ChatRoom,
        related_name=_("messages"),
        on_delete=models.CASCADE
    )
    context = models.TextField(
        verbose_name=_("Contexto da mensagem")
    )
    
    class Meta:
        verbose_name = _("Mensagem")
        verbose_name_plural = _("Mensagens")
        
    def __str__(self):
        return f"Usuário: {self.user.username} - Sala: {self.chat_room.slug}"
    

class Chat(TimestampModel):
    chat_room = models.OneToOneField(
        verbose_name=_("Sala de Conversa"),
        to=ChatRoom,
        related_name=_("chat"),
        on_delete=models.CASCADE
    )
    users = models.ManyToManyField(
        verbose_name=_("Usuários"),
        to=User,
        related_name=_("chats")
    )

    class Meta:
        verbose_name = _("Conversa")
        verbose_name_plural = _("Conversas")
