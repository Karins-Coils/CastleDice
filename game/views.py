from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from game.forms import ChooseGameForm
from game.models import Game
from game.solo_ai import JoanAI
from playermat.models import PlayerMat


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

        if data['game_choice'] == "id":
            old_game = Game.objects.get(pk=int(data["game_id"]))
            if old_game:
                self.game_obj = old_game
                self.game_type = "old"
                user = self.request.user

                # confirm a playermat exists for this player + game
                # otherwise, make a new one
                try:
                    playermat = PlayerMat.objects.get(player=user, game=old_game)
                except PlayerMat.DoesNotExist:
                    playermat = PlayerMat(player=user, game=old_game)
                    playermat.save()

        if not self.game_obj:
            new_game = Game()
            if data['game_choice'] == "solo":
                new_game.is_solo_game = True
            new_game.save()
            new_player_mat = PlayerMat(player=self.request.user, game=new_game)
            new_player_mat.save()

            if new_game.is_solo_game:
                joan_playermat = PlayerMat(player=JoanAI.get_user_joan(),
                                           game=new_game)
                joan_playermat.save()

            self.game_obj = new_game
            self.game_type = "new"

        return super(ChooseGameView, self).form_valid(form)

    def get_success_url(self):
        # get current turn from db or '1'
        if self.game_type is "new":
            return reverse('new_game', kwargs={'game_id': self.game_obj.id})
        else:
            return reverse('continue_game', kwargs={'game_id': self.game_obj.id})

        # return reverse('choose_dice', kwargs={'turn_no': 1})


class NewGameView(TemplateView):
    template_name = "start.html"

    def dispatch(self, request, *args, **kwargs):
        game = Game.objects.get(id=kwargs['game_id'])

        # if GET, setup choice dice for the first time, if empty
        if request.method is "GET":
            game.setup_choice_dice_for_turn()

        request.game = game
        request.playermat = game.playermat_set.get(player=self.request.user)

        return super(NewGameView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(NewGameView, self).get_context_data(**kwargs)
        context["new"] = True
        context["game_id"] = int(self.kwargs["game_id"])
        context["game_turn"] = 1
        return context


class ContinueGameView(TemplateView):
    template_name = "start.html"

    def dispatch(self, request, *args, **kwargs):
        game = Game.objects.get(id=kwargs['game_id'])

        # if GET, setup choice dice for the first time, if empty
        if request.method is "GET":
            game.setup_choice_dice_for_turn()

        request.game = game
        request.playermat = game.playermat_set.get(player=self.request.user)

        return super(ContinueGameView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ContinueGameView, self).get_context_data(**kwargs)
        context["game_id"] = int(self.kwargs["game_id"])
        return context


class PlayOrderView(TemplateView):
    template_name = "player_order.html"
    # if not solo + turn = 1 + current_player not set, players must roll
    # else, call game.determine_player_order + display for round

    def get_context_data(self, **kwargs):
        game = Game.objects.get(id=kwargs['game_id'])
        playermats = game.playermat_set.all().order_by('player_order')

        context = super(PlayOrderView, self).get_context_data(**kwargs)
        context['game_id'] = kwargs['game_id']
        context['players'] = [User.objects.get(id=playermat.player_id)
                              for playermat in playermats]
        return context
