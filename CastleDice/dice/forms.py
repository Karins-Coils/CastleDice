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


#die_choices = [
#    (Wood, Wood),
#    (Stone, Stone),
#    (Gold, Gold),
#    (Land, Land),
#    (Iron, Iron)
#]


class ChooseDiceForm(forms.Form):
    choice_dice = forms.MultipleChoiceField(label="Dice Choices", widget=forms.CheckboxSelectMultiple)
    given_dice = forms.MultipleChoiceField(label="Given Dice", widget=forms.CheckboxSelectMultiple)


    def __init__(self, *args, **kwargs):
        #if len(kwargs) > 0:
        #    dice_list = kwargs.pop('chooseabledice')
        #else:
        dice_list = [Wood, Stone, Gold, Land]
        dice_list2 = [Wood, Iron, Iron]
        super(ChooseDiceForm, self).__init__(*args, **kwargs)
        #self.form.fields['field_name'].widget = forms.HiddenInput()
        self.fields['choice_dice'].choices = self.make_choices(dice_list)
        self.fields['given_dice'].choices = self.make_choices(dice_list2)


    # preps the form choices for user
    def make_choices(self, d_list):
        d_choices = []
        for die in d_list:
            if die == Wood:
                d_choices.append((Wood, Wood))
            elif die == Stone:
                d_choices.append((Stone, Stone))
            elif die == Gold:
                d_choices.append((Gold, Gold))
            elif die == Land:
                d_choices.append((Land, Land))
            elif die == Iron:
                d_choices.append((Iron, Iron))
        return d_choices