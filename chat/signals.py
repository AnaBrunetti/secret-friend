# code
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings 

from accounts.models import User
from chat.models import Chat, ChatRoom

 
@receiver(post_save, sender=User)
def create_chat_bot(sender, instance, created, **kwargs):
    if created:
        if not User.objects.filter(role=User.ROLE_BOT).exists():
            User.objects.create(
                username=settings.BOT_NAME,
                email=settings.BOT_EMAIL,
                role=User.ROLE_BOT,
                password=settings.BOT_PASSWORD
            )

        bot_user = User.objects.filter(role=User.ROLE_BOT).first()
        slug = f"{bot_user.username}-{instance.username}"
        chat_room = ChatRoom.objects.create(
            slug=slug
        )
        chat = Chat.objects.create(
            chat_room=chat_room
        )
        chat.users.add(bot_user)
        chat.users.add(instance)
