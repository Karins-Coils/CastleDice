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
        # fetch turn_no from url
        if kwargs['turn_no']:
            self.turn_no = int(kwargs['turn_no'])
        return super(ChooseDiceView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        # attach turn_no to form vars
        kwargs = super(ChooseDiceView, self).get_form_kwargs()
        if self.turn_no:
            kwargs['initial']['turn_no'] = self.turn_no
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ChooseDiceView, self).get_context_data(**kwargs)
        context["game_id"] = int(self.kwargs["game_id"])
        context["cur_turn"] = self.turn_no
        return context

    def form_valid(self, form):
        game_obj = Game.objects.get(pk=int(self.kwargs['game_id']))
        user = self.request.user

        # retrieve player mat if available, else make new one
        try:
            player_mat = PlayerMat.objects.get(game=game_obj, user=user)
        except PlayerMat.DoesNotExist:
            player_mat = PlayerMat(game=game_obj, user=user)

        number_choice_die = int(
            TURN[int(self.kwargs['turn_no'])]['no_choices']
        )
        full_dice_list = form.cleaned_data['given_dice'] + \
                         [form.cleaned_data['choice_die'+str(x)]
                          for x in range(1, number_choice_die+1)]
        rolled_dice = {}
        for d in full_dice_list:
            rolled_d = Die(d).roll_die()
            if d in rolled_dice:
                rolled_dice[d].append(rolled_d)
            else:
                rolled_dice[d] = [rolled_d]

        game_obj.turn_no = self.kwargs['turn_no']
        game_obj.phase_no = 3
        game_obj.save()
        player_mat.dice_rolled = rolled_dice
        player_mat.save()
        return super(ChooseDiceView, self).form_valid(form)

    def get_success_url(self):
        return reverse('rolldice', kwargs={
            'game_id': int(self.kwargs['game_id']),
            'turn_no': int(self.kwargs['turn_no']),
        })


class RollDiceView(TemplateView):
    template_name = "rolldice.html"

    def get_context_data(self, **kwargs):
        # add error checking for getting game/user
        game_obj = Game.objects.get(pk=int(self.kwargs['game_id']))
        user = self.request.user

        # add error checking for getting playermat
        player_mat = PlayerMat.objects.get(game=game_obj, user=user)

        context = super(RollDiceView, self).get_context_data(**kwargs)
        if self.kwargs['turn_no']:
            turn_no = int(self.kwargs['turn_no'])
            context["game_id"] = self.kwargs['game_id']
            context["cur_turn"] = turn_no
            context["nxt_turn"] = turn_no+1

        # loop through dice in dice_rolled and move them to world_pool
        context['rolled_dice'] = player_mat.dice_rolled

        game_obj.phase_no = 4
        game_obj.world_pool = {
            k: [d for d in die_list if not Die.is_barbarian(d)]
            for k, die_list in player_mat.dice_rolled.items()
        }

        player_mat.dice_rolled = {
            k: [d for d in die_list if Die.is_barbarian(d)]
            for k, die_list in player_mat.dice_rolled.items()
        }
        game_obj.save()
        player_mat.save()

        return context


class GatherDiceView(FormView):
    template_name = 'gatherdice.html'
    form_class = GatherDiceForm
    game_id = None
    turn_no = None
    round_no = None

    def dispatch(self, request, *args, **kwargs):
        # fetch turn_no from url
        if kwargs['game_id']:
            self.game_id = int(kwargs['game_id'])
        if kwargs['turn_no']:
            self.turn_no = int(kwargs['turn_no'])
        # if kwargs['round_no']:
            # self.round_no = int(kwargs['round_no'])
        return super(GatherDiceView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        # attach turn_no to form vars
        kwargs = super(GatherDiceView, self).get_form_kwargs()
        if self.game_id:
            kwargs['initial']['game_id'] = self.game_id
        if self.turn_no:
            kwargs['initial']['turn_no'] = self.turn_no

        return kwargs

    def get_context_data(self, **kwargs):
        context = super(GatherDiceView, self).get_context_data(**kwargs)
        context["game_id"] = self.game_id
        context["turn_no"] = self.turn_no
        # context["round_no"] = self.round_no

        return context

    def form_valid(self, form):
        game_obj = Game.objects.get(pk=int(self.kwargs['game_id']))
        user = self.request.user

        # retrieve player mat if available, else make new one
        try:
            player_mat = PlayerMat.objects.get(game=game_obj, user=user)
        except PlayerMat.DoesNotExist:
            player_mat = PlayerMat(game=game_obj, user=user)

        # remove user gathered die from the world_pool
        data = form.cleaned_data
        # store user gathered die in playermat dice_rolled


        game_obj.save()
        player_mat.save()
        return super(GatherDiceView, self).form_valid(form)

    def get_success_url(self):
        return reverse('gatherdice', kwargs={
            'game_id': int(self.kwargs['game_id']),
            'turn_no': int(self.kwargs['turn_no']),
        })