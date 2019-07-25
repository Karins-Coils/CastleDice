from django.contrib import admin
from django.urls import include, path

from CastleDice.game.views import (
    HomeView,
    ChooseGameView,
    ContinueGameView,
    NewGameView,
    PlayOrderView,
    WaitingView,
    PassPhaseView,
)
from CastleDice.die.views import ChooseDiceView, RollDiceView, GatherDiceView

# , ChooseDiceForm, RollDiceView

admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'CastleDice.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    path("", HomeView.as_view(), name="home"),
    path("accounts/", include("allauth.urls")),
    # choose/start a game
    path("start", ChooseGameView.as_view(), name="start"),
    path("game_<int:game_id>/start", NewGameView.as_view(), name="new_game"),
    path(
        "game_<int:game_id>/continue", ContinueGameView.as_view(), name="continue_game"
    ),
    # player order of Turn
    path(
        "game_<int:game_id>/player_order", PlayOrderView.as_view(), name="player_order"
    ),
    # choose phase of game
    path("game_<int:game_id>/choose", ChooseDiceView.as_view(), name="choose_dice"),
    # roll phase of game
    path("game_<int:game_id>/rolled", RollDiceView.as_view(), name="roll_dice"),
    # gather phase of game
    path("game_<int:game_id>/gather", GatherDiceView.as_view(), name="gather_dice"),
    # wait for other player during game
    path("game_<int:game_id>/waiting", WaitingView.as_view(), name="waiting"),
    # pass view, to temporary advance through missing phases
    path("game_<int:game_id>/pass_phase", PassPhaseView.as_view(), name="pass_phase"),
    path("porkchop/", admin.site.urls),
]
