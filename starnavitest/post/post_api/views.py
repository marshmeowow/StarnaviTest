from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions
from post.models import Post
from .custom_permissions import IsOwnerOrReadOnly
from .serializers import PostSerializer
from .mixins import LikedMixin


class PostsView(LikedMixin, generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, author=self.request.user.username)


class PostsDeleteView(generics.RetrieveDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.all()


class PostViewSet(LikedMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
