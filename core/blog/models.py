from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    class CategoryStatus(models.TextChoices):
        ENABLE = "ENABLE", "enable"
        DISABLE = "DISABLE", "disable"

    id = models.SmallAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    title = models.CharField(max_length=68, blank=True, null=True)
    slug = models.CharField(max_length=100, blank=True, null=True, unique=True)
    status = models.CharField(max_length=15, choices=CategoryStatus.choices, default=CategoryStatus.ENABLE)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'categories'
        verbose_name = 'category'
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title


class Post(models.Model):
    class PostStatus(models.TextChoices):
        DRAFT = "DRAFT", "draft"
        PUBLISHED = "PUBLISHED", "published"
        DELETED = "DELETED", "deleted"

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    title = models.CharField(max_length=68, blank=True, null=True)
    symbol = models.CharField(max_length=20, blank=True, null=True, unique=True)
    image = models.ImageField(blank=True, null=True, upload_to='uploads/')
    status = models.CharField(max_length=15, choices=PostStatus.choices, default=PostStatus.DRAFT)
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'posts'
        verbose_name = 'post'
        verbose_name_plural = 'Posts'

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title


