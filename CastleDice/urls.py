from django.conf.urls import patterns, include, url
from dice.views import HomeView, ChooseDiceView, RollDiceView
#, ChooseDiceForm, RollDiceView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', HomeView.as_view(), name='home'),
    # url(r'^CastleDice/', include('CastleDice.foo.urls')),
    url(r'^choosedice/(?P<turn_no>[\d])/$', ChooseDiceView.as_view(), name='choosedice'),
    url(r'^rolldice/(?P<turn_no>[\d])/(?P<dice_to_roll>[\w-]+)/$', RollDiceView.as_view(), name='rolldice'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
