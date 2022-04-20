from django.shortcuts import get_object_or_404
from rest_framework import mixins, serializers
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Article, Comment
from .serializers import (ArticleSerializer, CommentCreateSerializer,
                          CommentGetThirdPlusDepthSerializer)


class ArticletViewSet(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    """Вьюсэт для создания статьи и получения статьи по id с вложенными
    комментариями, где depth_level от 1 до 3."""

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class CreateCommentOnArticleAPIView(CreateAPIView):
    """Создает комментарий для статьи. Получает id статьи из URL."""

    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer

    def perform_create(self, serializer):
        article = get_object_or_404(Article, pk=self.kwargs.get("article_id"))
        serializer.save(article=article)


class CreateSubCommentAPIView(CreateAPIView):
    """Создает ответ для комментария. Получает id родительского комментария из URL.
    Получает id статьи из родительского комментария."""

    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer

    def perform_create(self, serializer):
        parent_comment = get_object_or_404(Comment, pk=self.kwargs.get("comment_id"))
        article = get_object_or_404(Article, pk=parent_comment.article.id)
        serializer.save(parent=parent_comment, article=article)


class GetSubCommentAPIView(RetrieveAPIView):
    """Получение комментария по id и всех вложенных коментариев.
    Переопределен метод retrive, можно запрашивать комментарий
    только 3 уровня вложенности."""

    queryset = Comment.objects.all()
    serializer_class = CommentGetThirdPlusDepthSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.depth_level != 3:
            raise serializers.ValidationError(
                {"depth_level": "уровень вложенности коментария должен быть 3."}
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
