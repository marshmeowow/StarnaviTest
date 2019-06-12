from rest_framework import serializers
from django.contrib.auth import get_user_model
from post.models import Post


class PostSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ['url',
                  'pk',
                  'author',
                  'content',
                  'timestamp',
                  'total_likes']
        read_only_fields = ('author',)

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)


User = get_user_model()


class FanSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'username',
            'full_name',]

    def get_full_name(self, obj):
        return obj.get_full_name()
