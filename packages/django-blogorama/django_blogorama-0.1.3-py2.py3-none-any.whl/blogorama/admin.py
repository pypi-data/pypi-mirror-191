from django.contrib import admin

from .models import Post, Tag, TagSuggestion, Comment, Vote, Rating, Save, Flag, PostFlag, Ban, Topic

admin.site.register(Post)
admin.site.register(Topic)
admin.site.register(Tag)
admin.site.register(TagSuggestion)
admin.site.register(Comment)
admin.site.register(Vote)
admin.site.register(Rating)
admin.site.register(Save)
admin.site.register(Flag)
admin.site.register(PostFlag)
admin.site.register(Ban)
