
from dieClass import Die
from CD_globals import TURN
from game.models import Game, PlayerMat
from django.views.generic.base import TemplateView
from die.forms import ChooseDiceForm
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse


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
            rolled_die = Die(d).roll_die()
            if d in rolled_dice:
                rolled_dice[d].append(rolled_die)
            else:
                rolled_dice[d] = [rolled_die]

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

        # loop through dice in dice_rolled and move them to worldpool

        context['rolled_dice'] = player_mat.dice_rolled
        return context

