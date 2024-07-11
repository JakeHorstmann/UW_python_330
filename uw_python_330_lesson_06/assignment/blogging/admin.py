from django.contrib import admin
from blogging.models import Post, Category


class CategoryInLine(admin.TabularInline):
    model = Category.posts.through


class PostAdmin(admin.ModelAdmin):
    inlines = [CategoryInLine]


class CategoryAdmin(admin.ModelAdmin):
    exclude = ["posts"]


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
