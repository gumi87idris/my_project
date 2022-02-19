from django.contrib import admin

from main.models import CodeImage, Post, Reply, Comment


class ImageInline(admin.TabularInline):
    model = CodeImage
    min_num = 1
    max_num = 10


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [ImageInline,]


admin.site.register(Reply)
admin.site.register(Comment)







