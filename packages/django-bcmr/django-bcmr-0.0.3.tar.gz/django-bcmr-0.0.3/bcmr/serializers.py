from rest_framework import serializers

from django.conf import settings

from bcmr.models import *


class EmptySerializer(serializers.Serializer):
    pass


class CashTokenSerializer(serializers.ModelSerializer):
    time = serializers.SerializerMethodField()
    token = serializers.SerializerMethodField()
    uris = serializers.SerializerMethodField()

    class Meta:
        model = Token
        fields = (
            'name',
            'description',
            'time',
            'token',
            'status',
            'uris',
        )

    def get_time(self, obj):
        return {
            'begin': obj.date_created
        }

    def get_token(self, obj):
        return {
            'category': obj.category,
            'symbol': obj.symbol,
            'decimals': obj.decimals
        }

    def get_uris(self, obj):
        if obj.icon:
            return {
                'icon': f'{settings.DOMAIN}{obj.icon.url}'
            }
        return {}


class RegistrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Registry
        fields = (
            'name',
            'description',
            'tokens',
        )


class BcmrRegistrySerializer(serializers.ModelSerializer):
    version = serializers.SerializerMethodField()
    latestRevision = serializers.SerializerMethodField()
    registryIdentity = serializers.SerializerMethodField()
    identities = serializers.SerializerMethodField()

    class Meta:
        model = Registry
        fields = (
            'version',
            'latestRevision',
            'registryIdentity',
            'identities',
        )

    def get_version(self, obj):
        return {
            'major': obj.major,
            'minor': obj.minor,
            'patch': obj.patch
        }

    def get_latestRevision(self, obj):
        return obj.latest_revision

    def get_registryIdentity(self, obj):
        return {
            'name': obj.name,
            'description': obj.description,
            'time': {
                'begin': obj.date_created
            }
        }

    def get_identities(self, obj):
        tokens = obj.tokens.all()
        identities = {}

        for token in tokens:
            t = CashTokenSerializer(token).data
            identities[t['token']['category']] = [t]

        return identities
