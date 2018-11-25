from django.db import models
from django.utils import timezone
from django.urls import reverse
import misaka

# Create your models here.
class Post(models.Model):

    author = models.ForeignKey('accounts.User',related_name='posts',on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    content = models.TextField()
    created_date = models.DateTimeField()
    edited_date = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("blog_app:detail",kwargs={"pk":self.pk})

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_date=timezone.now()
        self.content = misaka.html(self.content)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_date']


class Comment(models.Model):
    author = models.ForeignKey('accounts.User',related_name="comments",on_delete=models.CASCADE)
    post = models.ForeignKey('blog_app.Post',related_name="comments",on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField()
    edited_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_date=timezone.now()

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_app:detail',kwargs={'pk':self.post.pk})


    class Meta:
        ordering = ['-created_date']


class Like(models.Model):
    post = models.ForeignKey('blog_app.Post',related_name='likes',on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.User',related_name='likes',on_delete=models.CASCADE)

    def __str__(self):
        return "User:" + self.user.username + ", Likes: " + self.post.title

    class Meta:
        unique_together = ['user','post']
