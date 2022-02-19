from django.db import models

from account.models import CustomUser


class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='posts')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('created',)


class CodeImage(models.Model):
    image = models.ImageField(upload_to='post_images')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')


class Reply(models.Model):      # ответ на пост
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='replies')
    body = models.TextField()
    # картинка для ответа
    image = models.ImageField(upload_to='reply_images')
    author = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='replies')
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(CustomUser, related_name='likers', blank=True)

    def __str__(self):
        return f'{self.body[:15]}...'


class Comment(models.Model):
    comment = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='comments')
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, related_name='comments')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment


