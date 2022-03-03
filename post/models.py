from django.db import models
from django.contrib.auth import get_user_model
from users.models import Profile
# Create your models here.
class Post(models.Model):

    title = models.TextField(max_length=100) 
    created_by = models.ForeignKey(Profile, related_name='posts_created', on_delete=models.CASCADE) 
    description = models.TextField() 
    date_posted_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts' 
    
    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    user_id = models.ForeignKey(Profile, related_name="profile_comments", null=True, on_delete=models.SET_NULL) 
    content = models.TextField() 
    post_associated_id = models.ForeignKey(Post, related_name = 'post_comments', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'

    def __str__(self) -> str:
        return self.user_id 


class Like(models.Model):

    liked_by = models.ForeignKey(Profile, related_name="profile_likes", on_delete=models.CASCADE)

    posts_liked = models.ForeignKey(Post, related_name="post_likes", on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['liked_by', 'posts_liked'], name="unique_like"),
        ]