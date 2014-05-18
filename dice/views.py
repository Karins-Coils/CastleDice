
import diceClass
from diceClass import Die
import CD_globals as CD
from django.views.generic.base import TemplateView
from dice.forms import ChooseDiceForm
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse


# Resources
## Building Materials
Wood = CD.Wood
Stone = CD.Stone
Gold = CD.Gold
Land = CD.Land
Iron = CD.Iron
## Animals
Horse = CD.Horse
Pig = CD.Pig
Cow = CD.Cow
Chicken = CD.Chicken
## Lone Barbarian
Barbarian = CD.Barbarian


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        return context


class ChooseDiceView(FormView):
    template_name = 'choosedice.html'
    form_class = ChooseDiceForm
    turn_no = 00

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
        context["cur_turn"] = self.turn_no
        return context

    def form_valid(self, form):
        number_choice_die = int(CD.turn[int(self.kwargs['turn_no'])]['no_choices'])
        full_dice_list = form.cleaned_data['given_dice']
        for x in range(1, number_choice_die+1):
            full_dice_list.append(form.cleaned_data['choice_die'+str(x)])
        self.dice_to_roll = prepUrlFromDice(full_dice_list)
        return super(ChooseDiceView, self).form_valid(form)

    def get_success_url(self):
        return reverse('rolldice', kwargs={'dice_to_roll': self.dice_to_roll, 'turn_no': int(self.kwargs['turn_no'])})


class RollDiceView(TemplateView):
    template_name = "rolldice.html"

    def get_context_data(self, **kwargs):
        context = super(RollDiceView, self).get_context_data(**kwargs)
        turn_no = int(self.kwargs['turn_no'])
        context["cur_turn"] = turn_no
        context["nxt_turn"] = turn_no+1
        dice_url = self.kwargs['dice_to_roll']
        dice_to_roll = parseDiceUrl(dice_url)
        rolled_dice = []
        for d in dice_to_roll:
            roll_me = Die(d)
            rolled_dice.append((d, roll_me.roll_die()))
        totals = diceClass.total_dice(rolled_dice)
        context['rolled_dice'] = rolled_dice
        context['totals'] = totals
        return context


def prepUrlFromDice(dice_list):
    url = "-".join(dice_list)
    return url

def parseDiceUrl(url):
    dice_list = url.split("-")
    return dice_list
