from rest_framework import serializers

from .models import Article, Comment


class CommentCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания комментария."""

    class Meta:
        model = Comment
        fields = ("text",)


class RecursiveField(serializers.Serializer):
    """Сериализатор для рекурсивного отображения вложенных экземпляров."""

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentGetFirstThirdDepthSerializer(serializers.ModelSerializer):
    """Сериализатор для выдачи комментариев, где вложенные экземпляры
    имеют depth_level от 1 до 3."""

    comments = RecursiveField(
        many=True, read_only=True, source="first_third_level_depth_comment_tree"
    )

    class Meta:
        model = Comment
        fields = "__all__"


class ArticleSerializer(serializers.ModelSerializer):
    """Сериализатор для выдачи статьи и вложенных комментариев
    (depth_level от 1 до 3). Метод get_comments убирает дублирование комментов."""

    comments = serializers.SerializerMethodField()

    def get_comments(self, obj):
        queryset = Comment.objects.filter(article_id=obj.id, parent_id=None)
        serializer = CommentGetFirstThirdDepthSerializer(
            queryset, many=True, read_only=True
        )
        return serializer.data

    class Meta:
        model = Article
        fields = "__all__"


class CommentGetThirdPlusDepthSerializer(serializers.ModelSerializer):
    """Сериализатор для выдачи комментариев, где вложенные экземпляры
    имеют depth_level от 3."""

    comments = RecursiveField(
        many=True, read_only=True, source="third_plus_level_depth_comment_tree"
    )

    class Meta:
        model = Comment
        fields = "__all__"
