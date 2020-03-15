from django.db import models

from django.dispatch import receiver
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db.models.signals import post_save

# Create your models here.
class CustomUserManager(BaseUserManager):
    def _create_user(self, phone, password, **extra_fields):
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, name, phone, password=None):
        return self._create_user(phone, password, name=name)

    def create_superuser(self, name, phone, password=None):
        return self._create_user(phone, password, name=name, is_staff=True, is_superuser=True)



class CustomUser(PermissionsMixin, AbstractBaseUser):
    name = models.CharField(max_length=25, blank=False)
    phone = models.CharField(max_length=13, blank=False, unique=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

    def get_full_name(self):
        return self.phone

    def get_short_name(self):
        return self.phone

class FeedItem(models.Model):
    image = models.ImageField()
    title = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    link = models.CharField(max_length=120)

    def __str__(self):
        return self.title

    def number_of_comments(self):
        return Comment.objects.filter(post_connected=self).count()

class Comment(models.Model):
    content = models.TextField(max_length=150)
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post_connected = models.ForeignKey(FeedItem, on_delete=models.CASCADE)

class Report(models.Model):
    content = models.TextField(max_length=150)
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post_connected = models.ForeignKey(FeedItem, on_delete=models.CASCADE)

class Collection(models.Model):
    description = models.TextField(max_length=150)
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post_connected = models.ForeignKey(FeedItem, on_delete=models.CASCADE)

class Trend(models.Model):
    content = models.TextField(max_length=150)
    date_posted = models.DateTimeField(auto_now_add=True)
    country = models.TextField(max_length=150)

class Follow(models.Model):
    user = models.ForeignKey(CustomUser, related_name='user', on_delete=models.CASCADE)
    follow_user = models.ForeignKey(CustomUser, related_name='follow_user', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username}'


    def followers(self):
        return Follow.objects.filter(follow_user=self.user).count()

    def following(self):
        return Follow.objects.filter(user=self.user).count()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save()

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size(300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)