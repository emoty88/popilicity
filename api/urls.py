from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from rest_framework_jwt.views import (
    obtain_jwt_token,
    refresh_jwt_token,
    verify_jwt_token,
    )
from rest_framework import routers
from api.user import UserViewSet
from api.post import PostViewSet
from api.location import LocationViewSet
from api.interest import InterestViewSet
from api.comment import CommentViewSet
from api.reaction import ReactionViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'interests', InterestViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'reactions', ReactionViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^token-auth/', obtain_jwt_token),
    url(r'^token-refresh/', refresh_jwt_token),
    url(r'^token-verify/', verify_jwt_token),
]
