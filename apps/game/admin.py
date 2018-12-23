from django.contrib import admin

from .models import (
    Game,
    Tag,
    Purchase,
    Save,
    Highscore
)

admin.site.register(Game)
admin.site.register(Tag)
admin.site.register(Purchase)
admin.site.register(Save)
admin.site.register(Highscore)
