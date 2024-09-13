from django.db import models
from accounts.models import User


class Post(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
     # like_count = models.IntegerField()
    image = models.ImageField(upload_to="images/", blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content


class CommentLike(models.Model):

    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="liked_comments") ##여기
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.comment

#
