from django.contrib import admin

from .models import (
    Article, Comment, Category, ArticleImages, Rating
)

admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(ArticleImages)
admin.site.register(Rating)