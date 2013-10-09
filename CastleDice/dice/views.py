from .diceClass import Die
import diceClass
from django.views.generic.base import TemplateView
from dice.forms import ChooseDiceForm
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse

# Resources
## Building Materials
Wood = 'wood'
Stone = 'stone'
Gold = 'gold'
Land = 'land'
Iron = 'iron'
## Animals
Horse = 'horse'
Pig = 'pig'
Cow = 'cow'
Chicken = 'chicken'
## Lone Barbarian
Barbarian = 'barbarian'


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        return context


class ChooseDiceView(FormView):
    template_name = 'choosedice.html'
    form_class = ChooseDiceForm#()# [Wood, Land, Iron] )
    chosen_dice = {}

    def form_valid(self, form):
        self.chosen_dice = prepUrlFromDice(form.cleaned_data['Dice'])

        return super(ChooseDiceView, self).form_valid(form)

    def get_success_url(self):
        return reverse('rolldice', kwargs={'chosen_dice': self.chosen_dice})


class RollDiceView(TemplateView):
    template_name = "rolldice.html"

    def get_context_data(self, **kwargs):
        context = super(RollDiceView, self).get_context_data(**kwargs)
        dice_url = self.kwargs['chosen_dice']
        dice_to_roll = parseDiceUrl(dice_url)
        rolled_dice = {}
        for d in dice_to_roll:
            roll_me = Die(d)
            rolled_dice[d] = roll_me.roll_die()
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