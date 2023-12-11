from django.contrib import admin
from .models import Category, NewsArticle, UserPreferences, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'publication_date', 'category')
    search_fields = ('title', 'content')
    list_filter = ('category', 'publication_date')

@admin.register(UserPreferences)
class UserPreferencesAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)
    filter_horizontal = ('favorite_categories',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'publication_date', 'user', 'article', 'parent_comment')
    search_fields = ('content', 'user__username', 'article__title')
    list_filter = ('publication_date', 'article', 'user', 'parent_comment')
