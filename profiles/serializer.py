from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from . import models

class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FeedItem
        fields = ('id', 'image', 'title', 'timestamp', 'author', 'link')
        extra_kwargs = {
            'author':  {
                'read_only': True
            }
        }

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Follow
        fields = ('id', 'user', 'follow_user', 'date')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = ('id', 'phone', 'name', 'password')
        extra_kwargs = {
            'passord': {
                'write_only': True
            }
        }

        def create(self, validated_data):
            user = models.CustomUser(phone=validated_data['phone'], name=validated_data['name'])
            user.make_password(validated_data['password'])
            user.save(using=self._db)
            return user
            
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ('id', 'content', 'date_posted', 'author', 'post_connected')

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Report
        fields = ('id', 'content', 'date_posted', 'author', 'post_connected')

class TrendSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Trend
        fields = ('id', 'content', 'date_posted', 'country')

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Collection
        fields = ('id', 'description', 'date_posted', 'author', 'post_connected')
