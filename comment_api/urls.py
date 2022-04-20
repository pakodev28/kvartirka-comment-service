from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .views import (ArticletViewSet, CreateCommentOnArticleAPIView,
                    CreateSubCommentAPIView, GetSubCommentAPIView)

router_v1 = DefaultRouter()

router_v1.register("articles", ArticletViewSet)

urlpatterns = [
    path("v1/", include(router_v1.urls)),
    re_path(
        r"v1/articles/(?P<article_id>\d+)/comments/",
        CreateCommentOnArticleAPIView.as_view(),
    ),
    re_path(
        r"v1/comments/(?P<comment_id>\d+)/subcomments/",
        CreateSubCommentAPIView.as_view(),
    ),
    path(
        "v1/comments/<int:pk>/", GetSubCommentAPIView.as_view(), name="subcomments"
    ),
]
