from django.db import models
from users.models import User


class TimestampedModel(models.Model):
    """
    A mixin class add for 'create_date' and 'update_date'
    """

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BlogPost(TimestampedModel):
    title = models.CharField(max_length=200)
    content = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-publication_date"]

    def __str__(self):
        return self.title
