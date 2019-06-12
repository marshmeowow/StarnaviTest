from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from .views import PostsDeleteView, PostsView, PostViewSet

urlpatterns = [
    url(r'^$', PostsView.as_view(), name='post-list-create'),
    url(r'^(?P<pk>\d+)/$', PostsDeleteView.as_view(), name='post-del'),
]

router = DefaultRouter()
router.register(r'', PostViewSet)

urlpatterns += router.urls
