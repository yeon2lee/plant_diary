from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.fields.related import ManyToManyField

class Diary(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    pubDate = models.DateTimeField()
    content = models.TextField()
    image = models.ImageField(upload_to='diary/', blank=True, null=True)
    like = models.ManyToManyField(get_user_model(), related_name='like', blank=True)

    class Meta:
        ordering = ['-pubDate']

class Comment(models.Model):
    post_id = models.ForeignKey("Diary", on_delete=models.CASCADE, db_column="post_id")
    comment_id = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    body = models.TextField()