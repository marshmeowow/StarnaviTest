from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from rest_framework.reverse import reverse


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='likes',
                             on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    author = models.CharField(max_length=256, null=True)
    content = models.CharField(max_length=240)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = GenericRelation(Like)

    def __str__(self):
        return str(self.author)

    def get_api_url(self, request=None):
        return reverse('post-del', kwargs={'pk': self.pk}, request=request)

    @property
    def total_likes(self):
        return self.likes.count()

    @property
    def owner(self):
        return self.user
