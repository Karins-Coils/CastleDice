from django import forms
import diceClass

# Resources
## Building Materials
Wood = diceClass.Wood
Stone = diceClass.Stone
Gold = diceClass.Gold
Land = diceClass.Land
Iron = diceClass.Iron
## Animals
Horse = diceClass.Horse
Pig = diceClass.Pig
Cow = diceClass.Cow
Chicken = diceClass.Chicken
## Lone Barbarian
Barbarian = diceClass.Barbarian

def img(c):
    return "<img class='"+c+" mid'>"

die_choices = [
    ('W', Wood),# + ' ' + img(Wood)),
    ('S', Stone),# + ' ' + img(Stone)),
    ('G', Gold),
    ('L', Land),
    ('I', Iron)
]


class ChooseDiceForm(forms.Form):
    #die_list = []
    #woodDie = forms.ChoiceField(label="Wood Die", choices = ( ('W', "Wood")))
    #stoneDie = forms.ChoiceField(label="Stone Die")
    #goldDie = forms.ChoiceField(label="Gold Die")
    #landDie = forms.ChoiceField(label="Land Die")
    #ironDie = forms.ChoiceField(label="Iron Die")
    Dice = forms.MultipleChoiceField(label = "Dice Choices", widget = forms.CheckboxSelectMultiple, choices = die_choices)


    def __init__(self, *args, **kwargs):
        #if len(kwargs) > 0:
        #    dice_list = kwargs.pop('chooseabledice')
        #else:
        #    dice_list = [Wood, Stone, Gold, Land]
        #kwargs.setdefault('choices', {})['Dice'] = self.make_choices(dice_list)
        super(ChooseDiceForm, self).__init__(*args, **kwargs)

    #def process_choices(self):
    #    dice = []
    #    if self.get('woodDie'):
    #        dice.append('wood')
    #    if self.get('stoneDie'):
    #        dice.append('stone')
    #    if self.get('goldDie'):
    #        dice.append('gold')
    #    if self.get('landDie'):
    #        dice.append('land')
    #    if self.get('ironDie'):
    #        dice.append('iron')
    #    return dice

    def form_valid(self):
        pass



    # preps the form choices for user
    def make_choices(self, d_list):
        d_choices = []
        for die in d_list:
            if die == Wood:
                d_choices.append(('W', Wood))
            elif die == Stone:
                d_choices.append(('S', Stone))
            elif die == Gold:
                d_choices.append(('G', Gold))
            elif die == Land:
                d_choices.append(('L', Land))
            elif die == Iron:
                d_choices.append(('I', Iron))
        return d_choices