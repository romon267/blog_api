from django.db.models import base
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views as api_views

router = DefaultRouter()
router.register(r'posts', api_views.PostViewSet, basename='post')
router.register(r'comments', api_views.CommentViewSet, basename='comment')
router.register(r'users', api_views.UserViewSet, basename = 'user')
router.register(r'userfollowings', api_views.UserFollowingViewSet, basename = 'userfollowing')

urlpatterns = [
    path('', include(router.urls)),
    path('users/follow/<int:pk>/', api_views.UserFollow.as_view(), name='user-follow'),
]


urlpatterns += [
    path('api-auth/', include('rest_framework.urls'))
]