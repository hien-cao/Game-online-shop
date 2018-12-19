from django.contrib import admin

from .models import (
    Category,
    Developer,
    Game,
    GameCategory,
    LoadState,
    PlayDetails,
    Player,
    Score
)

admin.site.register(Category)
admin.site.register(Developer)
admin.site.register(Game)
admin.site.register(GameCategory)
admin.site.register(LoadState)
admin.site.register(PlayDetails)
admin.site.register(Player)
admin.site.register(Score)