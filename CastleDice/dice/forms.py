from django import forms

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

die_choices = [
    ('W', Wood),
    ('S', Stone),
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
        ##else:
        #dice_list = [Wood, Stone, Gold, Land]
        #self.make_choices2(dice_list)
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

    # preps the form choices for user
    def make_choices(self, die, index):
        if die == Wood:
            self.die_list.append(forms.BooleanField(label="Wood Die"))
        elif die == Stone:
            self.die_list.append(forms.BooleanField(label="Stone Die"))
        elif die == Gold:
            self.die_list.append(forms.BooleanField(label="Gold Die"))
        elif die == Land:
            self.die_list.append(forms.BooleanField(label="Land Die"))
        elif die == Iron:
            self.die_list.append(forms.BooleanField(label="Iron Die"))

    def make_choices2(self, d_list):
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
        self.Dice = forms.MultipleChoiceField(label="Dice Choices", choices = d_choices)