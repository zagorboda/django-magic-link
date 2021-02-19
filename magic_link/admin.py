from django.contrib import admin

from .models import MagicLinkHash


class MagicLinkHashAdmin(admin.ModelAdmin):
    readonly_fields = ('user_id', 'user_email', 'token_hash', 'created_at',  'hits')


admin.site.register(MagicLinkHash, MagicLinkHashAdmin)
