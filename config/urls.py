from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView

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
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path(
        "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    ),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("castledice.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    # Your stuff: custom urls includes go here

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
    # path("porkchop/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
