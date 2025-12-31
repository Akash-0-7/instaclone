from django.contrib import admin

from . models import *


admin.site.register(Login)
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Likes)
admin.site.register(Follow)
admin.site.register(Notification)