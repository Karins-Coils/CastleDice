from django.conf.urls import include, url
from game.views import HomeView, ChooseGameView, ContinueGameView, NewGameView
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
    url(r'^start/$', ChooseGameView.as_view(), name='start'),
    url(r'^game_(?P<game_id>[\d])/start', NewGameView.as_view(), name="newgame"),
    url(r'^game_(?P<game_id>[\d])/continue', ContinueGameView.as_view(), name="continuegame"),

    # choose phase of game
    url(r'^game_(?P<game_id>[\d])/turn_(?P<turn_no>[\d])/choose/$',
        ChooseDiceView.as_view(), name="choosedice"),
    url(r'^game_(?P<game_id>[\d])/turn_(?P<turn_no>[\d])/choose/rolled/$',
        RollDiceView.as_view(), name="rolldice"),

    # gather phase of game
    url(r'^game_(?P<game_id>[\d])/turn_(?P<turn_no>[\d])/gather/$',
        GatherDiceView.as_view(), name="gatherdice"),

    url(r'^admin/', include(admin.site.urls)),
]
