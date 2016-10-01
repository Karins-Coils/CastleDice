from django.conf.urls import include, url
from game.views import HomeView, ChooseGameView, ContinueGameView,\
    NewGameView, PlayOrderView
from die.views import ChooseDiceView, RollDiceView, GatherDiceView
#, ChooseDiceForm, RollDiceView

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'CastleDice.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', HomeView.as_view(), name='home'),

    url(r'^accounts/', include('allauth.urls')),

    # choose/start a game
    url(r'^start$', ChooseGameView.as_view(), name='start'),
    url(r'^game_(?P<game_id>\d+)/start', NewGameView.as_view(), name="new_game"),
    url(r'^game_(?P<game_id>\d+)/continue', ContinueGameView.as_view(), name="continue_game"),

    # player order of Turn
    url(r'^game_(?P<game_id>\d+)/player_order$',
        PlayOrderView.as_view(), name="player_order"),

    # choose phase of game
    url(r'^game_(?P<game_id>\d+)/choose$',
        ChooseDiceView.as_view(), name="choose_dice"),

    # roll phase of game
    url(r'^game_(?P<game_id>\d+)/rolled$',
        RollDiceView.as_view(), name="roll_dice"),

    # gather phase of game
    url(r'^game_(?P<game_id>\d+)/gather$',
        GatherDiceView.as_view(), name="gather_dice"),

    url(r'^porkchop/', include(admin.site.urls)),
]
