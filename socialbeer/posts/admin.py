from django.contrib import admin

from socialbeer.posts.models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'author', 'pub_date', 'live')
    list_filter = ('pub_date', 'author')
    raw_id_fields = ('retweets', 'parent_post', 'author',)

admin.site.register(Post, PostAdmin)
