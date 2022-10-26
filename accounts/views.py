from django.contrib.auth import get_user_model
from rest_framework.decorators import permission_classes, action
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import ugettext_lazy as _
from accounts.serializers import (
    UserDetailSerializer,
)
from accounts.models import (
    User,
    Profissional
)

User = get_user_model()


@permission_classes([IsAuthenticated])
class UserDetailsView(RetrieveUpdateAPIView):
    serializer_class = UserDetailSerializer
    lookup_field = None

    def get_object(self):
        return self.request.user
