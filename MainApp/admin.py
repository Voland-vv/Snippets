from django.contrib import admin
from MainApp.models import Snippet, Comment, Language

admin.site.register(Snippet)
admin.site.register(Comment)
admin.site.register(Language)