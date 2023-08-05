from django.contrib import admin

from bcmr.models import *


admin.site.site_header = 'Django BCMR Admin'


class TokenAdmin(admin.ModelAdmin):
    list_display = [
        'category',
        'name',
        'symbol',
        'decimals',
        'status',
        'date_created',
    ]

class RegistryAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'description',
        'date_created',
        'latest_revision',
    ]


admin.site.register(Token, TokenAdmin)
admin.site.register(Registry, RegistryAdmin)
