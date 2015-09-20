from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from game.forms import ChooseGameForm
from game.models import Game

# Create your views here.

class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        return context

class ChooseGameView(FormView):
    # have form that self submits, redirects to /game_<>/turn_<>
    template_name = 'choosegame.html'
    form_class = ChooseGameForm
    game_obj = None
    game_type = None


    def form_valid(self, form):
        data = form.cleaned_data

        if data['game_choice'] != "new":
            old_game = Game.objects.get(pk=int(data["game_id"]))
            if old_game:
                self.game_obj = old_game
                self.game_type = "old"

        if not self.game_obj:
            new_game = Game(turn_no=1, phase_no=1)
            new_game.save()
            self.game_obj = new_game
            self.game_type = "new"

        return super(ChooseGameView, self).form_valid(form)

    def get_success_url(self):
        # get current turn from db or '1'
        if self.game_type is "new":
            return reverse('newgame', kwargs={'game_id': self.game_obj.id})
        else:
            return reverse('continuegame', kwargs={'game_id': self.game_obj.id})

        # return reverse('choosedice', kwargs={'turn_no': 1})

class NewGameView(TemplateView):
    template_name = "start.html"

    def get_context_data(self, **kwargs):
        context = super(NewGameView, self).get_context_data(**kwargs)
        context["new"] = True
        context["game_id"] = int(self.kwargs["game_id"])
        context["game_turn"] = 1
        return context

class ContinueGameView(TemplateView):
    template_name = "start.html"

    def get_context_data(self, **kwargs):
        context = super(ContinueGameView, self).get_context_data(**kwargs)
        context["game_id"] = int(self.kwargs["game_id"])
        game_obj = Game.objects.get(pk=int(self.kwargs["game_id"]))
        context["game_turn"] = game_obj.turn_no
        return context