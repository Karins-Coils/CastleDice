from django.conf.urls import patterns, include, url
from dice.views import HomeView, ChooseDiceView, RollDiceView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'castledice2.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^choosedice/(?P<turn_no>[\d])/$', ChooseDiceView.as_view(), name='choosedice'),
    url(r'^rolldice/(?P<turn_no>[\d])/(?P<dice_to_roll>[\w-]+)/$', RollDiceView.as_view(), name='rolldice'),

    url(r'^admin/', include(admin.site.urls)),
)
