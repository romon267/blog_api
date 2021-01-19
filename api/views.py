from rest_framework import generics, permissions, renderers, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.reverse import reverse
from api.models import Post, Comment, UserFollowing
from api.serializers import PostSerializer, UserSerializer, CommentSerializer, FollowersSerializer, FollowingSerializer
from django.contrib.auth.models import User
from .permissions import IsAuthorOrReadOnly

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'posts': reverse('post-list', request=request, format=format),
        'comments': reverse('comment-list', request=request, format=format),
    })


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True)
    def follow(self, request, *args, **kwargs):
        user = self.user
        follow = request.user
        UserFollowing.objects.create(user_id=user.id, following_user_id = follow.id)

    @action(detail=True)
    def unfollow(self, request, *args, **kwargs):
        user = self.user
        follow = request.user
        UserFollowing.objects.delete(user_id=user.id, following_user_id = follow.id)