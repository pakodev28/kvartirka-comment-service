from django.db import models


class DateMixin(models.Model):
    """Миксин добавления даты создания экземпляра"""

    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class Article(DateMixin):
    text = models.TextField(verbose_name="Текст статьи")

    def __str__(self):
        return self.text


class Comment(DateMixin):
    """Модель комментария. parent - первичный ключ на Comment(self).
    Переопределен метот save для автоматического расчета
    уровня вложенности(depth_level) экземпляра.
    first_third_level_depth_comment_tree и third_plus_level_depth_comment_tree -
    методы для, отсортированной по уровню вложенности, выдачи.
    """

    article = models.ForeignKey(
        Article,
        verbose_name="Статья",
        on_delete=models.CASCADE,
        related_name="comments",
        blank=True,
        null=True,
    )
    text = models.TextField()
    parent = models.ForeignKey(
        "self",
        related_name="comments",
        verbose_name="Ответ на комментарий",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    depth_level = models.PositiveSmallIntegerField(verbose_name="Уровень вложенности")

    def save(self, *args, **kwargs):
        if self.parent is None:
            self.depth_level = 1
        else:
            self.depth_level = self.parent.depth_level + 1
        super(Comment, self).save(*args, **kwargs)

    @property
    def first_third_level_depth_comment_tree(self):
        return self.comments.filter(depth_level__lte=3)

    @property
    def third_plus_level_depth_comment_tree(self):
        return self.comments.filter(depth_level__gt=3)

    def __str__(self):
        return self.text
