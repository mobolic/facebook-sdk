from django.core.urlresolvers import reverse
from django.db import models


class Post(models.Model):
    title = models.TextField(max_length=150)
    body = models.TextField()
    published = models.BooleanField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.id})
