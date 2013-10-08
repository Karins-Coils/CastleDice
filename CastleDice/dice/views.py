from .diceClass import Die
from django.views.generic.base import TemplateView
#from django.shortcuts import render_to_response
#from django.http import HttpResponseRedirect
#from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from dice.forms import ChooseDiceForm
from django.views.generic.edit import FormView

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

class RollDiceView(TemplateView):

    template_name = "rolldice.html"

    def get_context_data(self, **kwargs):
        context = super(RollDiceView, self).get_context_data(**kwargs)
        context['dice_choices'] = [ Wood, Stone, Gold, Land, Iron ]
        return context

class ChooseDiceView(FormView):
    template_name = 'choosedice.html'
    form_class = ChooseDiceForm #(chooseabledice=[Wood, Land, Iron])

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        dice = form.process_choices()
        for d in request.POST.getlist('dice'):
            roll_me = Die(d)
            dice[d] = roll_me.roll_die()
        return super(ChooseDiceView, self).form_valid(form)


#def home(request):
#
#    return render_to_response('home.html')

#@csrf_protect
#def rolldice(request):
#    c = {}
#    c.update(csrf(request))
#    dice = {}
#    for d in request.POST.getlist('dice'):
#        roll_me = Die(d)
#        dice[d] = roll_me.roll_die()
#
#    return render_to_response('rolldice.html', {'dice': dice}, c)
#
#@csrf_protect
#def choosedice(request):
#    dice =[ Wood, Stone, Gold, Land, Iron ]
#    return render_to_response('choosedice.html', {"dice_choices": dice})