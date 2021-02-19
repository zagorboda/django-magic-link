from django.db import models


class MagicLinkHash(models.Model):
    user_id = models.IntegerField(default=False)
    user_email = models.EmailField()
    token_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    hits = models.IntegerField(default=0)

