from rest_framework import generics, permissions, renderers, viewsets
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.reverse import reverse
from api.models import Post, Comment, UserFollowing
from api.serializers import PostSerializer, UserFollowingSerializer, UserSerializer, CommentSerializer, FollowersSerializer, FollowingSerializer
from django.contrib.auth.models import User
from .permissions import IsAuthorOrReadOnly

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'posts': reverse('post-list', request=request, format=format),
        'comments': reverse('comment-list', request=request, format=format),
        'followings': reverse('userfollowing-list', request=request, format=format)
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
    

class UserFollowingViewSet(viewsets.ModelViewSet):
    queryset = UserFollowing.objects.all()
    serializer_class = UserFollowingSerializer



class UserFollow(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        user = request.user
        follow = self.get_object(pk)
        UserFollowing.objects.create(user_id=user, following_user_id = follow)
        serializer = UserSerializer(follow)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        user = request.user
        follow = self.get_object(pk)
        connection = UserFollowing.objects.filter(user_id=user, following_user_id = follow).first()
        connection.delete()
        serializer = UserSerializer(follow)
        return Response(serializer.data)