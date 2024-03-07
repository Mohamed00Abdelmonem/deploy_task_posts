from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from simple_history.models import HistoricalRecords


#___________________________________________________________________________________


def user_upload_path(instance, filename):
    # Assuming 'user' is a ForeignKey in your model pointing to the User model
    user_id = instance.user.id
    return f'posts/user_{user_id}/{filename}'

class Post(models.Model):
    user = models.ForeignKey(User, related_name='post_user', on_delete=models.CASCADE)
    caption = models.TextField(max_length=3000)
    image = models.ImageField(upload_to=user_upload_path, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='like_post', null=True, blank=True)
    history = HistoricalRecords()

    def add_like(self, user):
        # Add a like to the post.
        if user not in self.likes.all():
            self.likes.add(user)
    def remove_like(self, user):
        # Remove a like from the post.
        if user in self.likes.all():
            self.likes.remove(user)
        
            
    def __str__(self) -> str:
        return self.caption
    
#___________________________________________________________________________________

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comment_post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='comment_user', on_delete=models.CASCADE)
    comment = models.CharField(max_length=400)
    created_at = models.DateTimeField(default=timezone.now)
    # reply = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.comment
#___________________________________________________________________________________

