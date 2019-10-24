from django.contrib import admin
from game.models import Player, Game, PlayerGameInfo
from django.forms import BaseInlineFormSet


class PlayerGameInfoInline(admin.TabularInline):
    model = PlayerGameInfo
    extra = 0


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    inlines = [PlayerGameInfoInline]
    list_display = ('id',)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    inlines = [PlayerGameInfoInline]
    list_display = ('id', 'guessed_number', 'active')
    list_filter = ('active',)