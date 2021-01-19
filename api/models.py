from django.db import models
from django.contrib.auth.models import User

class UserFollowing(models.Model):
    class Meta:
        constraints= [
            models.UniqueConstraint(fields=['user_id', 'following_user_id'], name='unique_following')
        ]
        ordering = ['-created']
        
    user_id = models.ForeignKey('auth.User', related_name='following', on_delete=models.SET_NULL, null=True,blank=True)
    following_user_id = models.ForeignKey('auth.User', related_name='followers', on_delete=models.SET_NULL, null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.user_id} is following {self.following_user_id}'

class Post(models.Model):
    title = models.CharField(max_length=150, blank=True)
    content = models.TextField()
    post_image = models.CharField(max_length=32, blank=True)
    author = models.ForeignKey('auth.User', related_name='posts', on_delete=models.SET_NULL, null=True)
    is_hidden = models.BooleanField(default=False)
    is_edited = models.BooleanField(default=False)
    date_posted = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-date_posted']

class Comment(models.Model):
    content = models.TextField()
    comment_image = models.CharField(max_length=32, blank=True)
    author = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    is_edited = models.BooleanField(default=False)
    date_posted = models.DateTimeField(auto_now_add=True)
    parent_post = models.ForeignKey('Post', on_delete=models.CASCADE)