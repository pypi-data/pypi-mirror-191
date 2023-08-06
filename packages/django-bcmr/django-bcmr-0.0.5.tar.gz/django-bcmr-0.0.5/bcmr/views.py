from django.core.exceptions import ImproperlyConfigured
from django.utils import timezone
from django.conf import settings
from django.shortcuts import render

from drf_yasg.utils import swagger_auto_schema

from rest_framework.response import Response
from rest_framework import viewsets, status

from bcmr.auth import HeaderAuthentication
from bcmr.utils import generate_auth_token
from bcmr.serializers import *
from bcmr.filters import *
from bcmr.models import *
from bcmr.forms import *

import logging
logger = logging.getLogger(__name__)


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
    
    @swagger_auto_schema(responses={200: BcmrRegistrySerializer})
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

 
def add_token(request):
    submitted = False
    message = ''

    if request.method == 'POST':
        queryDict = request.POST
        data = dict(queryDict.lists())

        category = data['category'][0]
        name = data['name'][0]
        description = data['description'][0]
        symbol = data['symbol'][0]
        decimals = int(data['decimals'][0])
        icon = data['icon'][0]
        
        if Token.objects.filter(category=category).exists():
            message = 'Token already exists!'
        else:
            token = Token(
                category=category,
                name=name,
                description=description,
                symbol=symbol,
                decimals=decimals,
                icon=icon
            )
            token.save()

            message = f'Token added!'

        submitted = True


    context = {
        'form': TokenForm(),
        'submitted': submitted,
        'message': message
    }
    return render(request, 'bcmr/add_token.html', context)
