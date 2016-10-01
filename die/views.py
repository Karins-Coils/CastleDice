from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from common.globals import TURN
from die.forms import ChooseDiceForm, GatherDiceForm
from dieClass import Die
from game.models import Game
from playermat.models import PlayerMat


class ChooseDiceView(FormView):
    template_name = 'choosedice.html'
    form_class = ChooseDiceForm
    turn_no = 00
    dice_to_roll = None

    def dispatch(self, request, *args, **kwargs):
        game = Game.objects.get(id=kwargs['game_id'])

        # if GET, setup choice dice for the first time, if empty
        if request.method == "GET":
            game.setup_choice_dice_for_turn()

        request.game_id = game.id
        self.turn_no = game.current_turn

        return super(ChooseDiceView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        game = Game.objects.get(id=self.request.game_id)
        playermat = PlayerMat.objects.get(player=self.request.user, game=game)

        # attach turn_no to form vars
        kwargs = super(ChooseDiceView, self).get_form_kwargs()
        kwargs['initial']['game'] = game
        kwargs['initial']['given_dice'] = playermat.choice_dice
        kwargs['initial']['no_choices'] = playermat.get_player_choice_extra_dice()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ChooseDiceView, self).get_context_data(**kwargs)
        context["game_id"] = int(self.kwargs["game_id"])
        context["cur_turn"] = self.turn_no
        return context

    def form_valid(self, form):
        # game = self.request.game
        game = Game.objects.get(id=int(self.kwargs['game_id']))
        user = self.request.user
        turn_no = game.current_turn

        # retrieve player mat if available, else make new one
        playermat = PlayerMat.objects.get(game=game, player=user)

        number_choice_die = playermat.get_player_choice_extra_dice()
        playermat.choice_dice = form.cleaned_data['given_dice'] + \
                                [form.cleaned_data['choice_die'+str(x)]
                                 for x in range(1, number_choice_die+1)]

        playermat.save()
        return super(ChooseDiceView, self).form_valid(form)

    def get_success_url(self):
        return reverse('roll_dice', kwargs={
            'game_id': int(self.kwargs['game_id']),
            # 'turn_no': int(self.kwargs['turn_no']),
        })


class RollDiceView(TemplateView):
    template_name = "rolldice.html"

    def get_context_data(self, **kwargs):
        # add error checking for getting game/user
        game_obj = Game.objects.get(pk=int(self.kwargs['game_id']))
        user = self.request.user

        # add error checking for getting playermat
        playermat = PlayerMat.objects.get(game=game_obj, player=user)

        context = super(RollDiceView, self).get_context_data(**kwargs)

        dice_rolled = playermat.roll_choice_dice()
        context['rolled_dice'] = dice_rolled

        game_obj.add_dice_to_world({
            k: [d for d in die_list if not Die.is_barbarian(d)]
            for k, die_list in dice_rolled.items()
        })
        game_obj.save()
        playermat.save()

        return context


class GatherDiceView(FormView):
    template_name = 'gatherdice.html'
    form_class = GatherDiceForm
    game_id = None
    turn_no = None
    round_no = None

    def dispatch(self, request, *args, **kwargs):
        # fetch turn_no from url
        self.game = Game.objects.get(id=int(kwargs['game_id']))
        return super(GatherDiceView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        # attach turn_no to form vars
        kwargs = super(GatherDiceView, self).get_form_kwargs()
        kwargs['initial']['game_id'] = self.game.id
        kwargs['initial']['turn_no'] = self.game.current_turn

        return kwargs

    def get_context_data(self, **kwargs):
        context = super(GatherDiceView, self).get_context_data(**kwargs)
        context["game_id"] = self.game.id
        context["turn_no"] = self.game.current_turn

        return context

    def form_valid(self, form):
        game_obj = Game.objects.get(pk=int(self.kwargs['game_id']))
        user = self.request.user

        # retrieve player mat if available, else make new one
        player_mat = PlayerMat.objects.get(game=game_obj, player=user)

        # remove user gathered die from the world_pool
        data = form.cleaned_data
        # store user gathered die in playermat dice_rolled

        game_obj.save()
        player_mat.save()
        return super(GatherDiceView, self).form_valid(form)

    def get_success_url(self):
        return reverse('gather_dice', kwargs={
            'game_id': int(self.kwargs['game_id']),
        })