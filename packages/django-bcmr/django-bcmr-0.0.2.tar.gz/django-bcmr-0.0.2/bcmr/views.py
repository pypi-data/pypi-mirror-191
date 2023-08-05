from django.core.exceptions import ImproperlyConfigured
from django.utils import timezone
from django.conf import settings

from rest_framework.response import Response
from rest_framework import viewsets, mixins

from bcmr.serializers import *
from bcmr.models import *


class TokenViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin
):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer


class RegistryViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin
):
    queryset = Registry.objects.all()
    serializer_class = EmptySerializer

    serializer_classes = {
        'create': RegistrySerializer,
        'list': BcmrRegistrySerializer,
        'update': RegistrySerializer,
        'partial_update': RegistrySerializer,
        'retrieve': BcmrRegistrySerializer
    }

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        instance.latest_revision = timezone.now()
        instance.save()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        bcmr = BcmrRegistrySerializer(instance)
        return Response(bcmr.data)

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()
