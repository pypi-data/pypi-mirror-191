from django.core.exceptions import ImproperlyConfigured
from django.utils import timezone
from django.conf import settings

from rest_framework.response import Response
from rest_framework import viewsets, status

from bcmr.auth import HeaderAuthentication
from bcmr.utils import generate_auth_token
from bcmr.serializers import *
from bcmr.filters import *
from bcmr.models import *


def get_or_create_owner(bcmr_auth_header):
    if bcmr_auth_header:
        return AuthToken.objects.get(id=bcmr_auth_header)
    else:
        return generate_auth_token()


class TokenViewSet(viewsets.ModelViewSet):
    queryset = Token.objects.all()
    filterset_class = TokenFilter
    filter_backends = (filters.DjangoFilterBackend, )
    authentication_classes = (HeaderAuthentication, )
    serializer_class = EmptySerializer
    serializer_classes = {
        'create': CashTokenSerializer,
        'list': RegistryIdentitySerializer,
        'update': CashTokenSerializer,
        'partial_update': CashTokenSerializer,
        'retrieve': RegistryIdentitySerializer
    }

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)            
        serializer.validated_data['owner'] = get_or_create_owner(request.META.get('HTTP_BCMR_AUTH'))
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()


class RegistryViewSet(viewsets.ModelViewSet):
    queryset = Registry.objects.all()
    filterset_class = RegistryFilter
    filter_backends = (filters.DjangoFilterBackend, )
    authentication_classes = (HeaderAuthentication, )
    serializer_class = EmptySerializer
    serializer_classes = {
        'create': RegistrySerializer,
        'list': NoOwnerRegistrySerializer,
        'update': RegistrySerializer,
        'partial_update': RegistrySerializer,
        'retrieve': BcmrRegistrySerializer
    }

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)            
        serializer.validated_data['owner'] = get_or_create_owner(request.META.get('HTTP_BCMR_AUTH'))
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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
