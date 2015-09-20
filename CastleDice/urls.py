from django.conf.urls import patterns, include, url
from game.views import HomeView, ChooseGameView, ContinueGameView, NewGameView
from die.views import ChooseDiceView, RollDiceView
#, ChooseDiceForm, RollDiceView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'CastleDice.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^choosedice/(?P<turn_no>[\d])/$', ChooseDiceView.as_view(), name='choosedice'),
    url(r'^rolldice/(?P<turn_no>[\d])/(?P<dice_to_roll>[\w-]+)/$', RollDiceView.as_view(), name='rolldice'),
    url(r'^start/$', ChooseGameView.as_view(), name='start'),
    url(r'^game_(?P<game_id>[\d])/start', NewGameView.as_view(), name="newgame"),
    url(r'^game_(?P<game_id>[\d])/continue', ContinueGameView.as_view(), name="continuegame"),

    url(r'^admin/', include(admin.site.urls)),
)
