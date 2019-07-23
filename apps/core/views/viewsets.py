from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

__all__ = (
    'SafeModelViewSet',
    'MultiSerializerViewSetMixin',
)


class SafeModelViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet based view with public access to list and single object
    and protected access for unsafe actions.
    """
    SAFE_ACTIONS = ('list', 'retrieve', )

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in self.SAFE_ACTIONS:
            permission_classes = []
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class MultiSerializerViewSetMixin(object):
    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super(MultiSerializerViewSetMixin, self).get_serializer_class()
