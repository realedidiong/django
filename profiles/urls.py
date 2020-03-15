from django.conf.urls import url
from django.conf.urls import include

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('login', views.LoginViewSet, basename='login-view')
router.register('feed', views.FeedViewSet, basename='feed-view')
router.register('users', views.UserViewSet, basename='user-view')
router.register('homefeed', views.HomeViewSet, basename='home-view')
router.register('follow', views.FollowViewSet, basename='follow-view')
router.register('comments', views.CommentViewSet, basename='comment-view')
router.register('collections', views.CollectionViewSet, basename='collection-view')
router.register('trend', views.TrendViewSet, basename='trend-view')
router.register('report', views.ReportViewSet, basename='report-view')

urlpatterns = [
    url(r'', include(router.urls))
]