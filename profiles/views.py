from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from . import serializer
from . import permissions
from . import models

# Create your views here.
class FeedViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializer.FeedSerializer
    permission_classes = (permissions.PostOwnStatus, IsAuthenticatedOrReadOnly)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'author',)
    queryset = models.FeedItem.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class FollowViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializer.FollowSerializer
    permission_classes = (permissions.PostOwnStatus, IsAuthenticatedOrReadOnly)
    queryset = models.Follow.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_queryset(self):
        user = self.request.user
        return models.Follow.objects.filter(user=user).order_by('-date')

class FollowersViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializer.FollowSerializer
    permission_classes = (permissions.PostOwnStatus, IsAuthenticatedOrReadOnly)
    queryset = models.Follow.objects.all()
    
    def get_queryset(self):
        user = self.request.user
        return models.Follow.objects.filter(follow_user=user).order_by('-date')

class HomeViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializer.FeedSerializer
    permission_classes = (permissions.PostOwnStatus, IsAuthenticatedOrReadOnly)
    
    def get_queryset(self):
        user = self.request.user
        qs = models.Follow.objects.filter(user=user)
        follows = [user]
        for obj in qs:
            follows.append(obj.follow_user)
        return models.FeedItem.objects.filter(author__in=follows).order_by('-timestamp')

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializer.UserSerializer
    authentication_classes = (TokenAuthentication,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('phone', 'name',)
    permission_classes = (permissions.UpdateOwnProfile,)
    queryset = models.CustomUser.objects.all()

class LoginViewSet(viewsets.ViewSet):
    serializer_class = AuthTokenSerializer
    def create(self, request):
        return ObtainAuthToken().post(request)

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializer.CommentSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = models.Comment.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('post_connected',)

class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = serializer.ReportSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = models.Report.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('post_connected', 'content')

class CollectionViewSet(viewsets.ModelViewSet):
    serializer_class = serializer.CommentSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = models.Collection.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('description')

    def get_queryset(self):
        user = self.request.user
        return models.Collection.objects.filter(author=user).order_by('-date_posted')

class TrendViewSet(viewsets.ModelViewSet):
    serializer_class = serializer.TrendSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = models.Trend.objects.all()

    def get_queryset(self):
        country = 'Nigeria'
        return models.Trend.objects.filter(country=country).order_by('-date_posted')