from django import forms
from django.forms import widgets
from django.forms.util import ValidationError
import diceClass

from itertools import chain
from django.utils.encoding import force_text
from django.utils.html import conditional_escape, format_html, format_html_join
from django.utils.safestring import mark_safe
from django.forms.util import flatatt

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

class CheckboxMultipleImgWidget(widgets.CheckboxSelectMultiple):

    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        output = []
        # Normalize to strings
        str_values = set([force_text(v) for v in value])
        first = True
        for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                label_for = format_html(' for="{0}"', final_attrs['id'])
            else:
                label_for = ''

            cb = widgets.CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
            option_value = force_text(option_value)
            rendered_cb = cb.render(name, option_value)
            option_label = force_text(option_label)
            output.append(format_html('<label{0}>{1} <img class="{2} mid"></label>',
                                      label_for, rendered_cb, option_label))
        output.append("<br>")
        return mark_safe('\n'.join(output))

class RadioImgWidget(widgets.RadioSelect):
    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name, type="radio")

        output = []
        for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                label_for = format_html(' for="{0}"', final_attrs['id'])
            else:
                label_for = ''
            if not (option_value is True or
                            option_value is False or
                            option_value is None or
                            value == ''):
                # Only add the 'value' attribute if a value is non-empty.
                final_attrs['value'] = force_text(option_value)
            option_label = force_text(option_label)
            output.append(
                format_html('<label{0}><input{1} /> <img class="{2} mid"> {3}</label><br>',
                            label_for, flatatt(final_attrs), option_label, option_label.capitalize()))

        return mark_safe('\n'.join(output))

class ChooseDiceForm(forms.Form):
    #choice_dice = forms.MultipleChoiceField(label="Dice Choices", widget=forms.CheckboxSelectMultiple)
    given_dice = forms.MultipleChoiceField(label="Given Dice", widget=CheckboxMultipleImgWidget({'style':"display:none", "checked":"checked"}))
    #choice_die1 = forms.ChoiceField(label="First Choice Die", widget=forms.RadioSelect)


    def __init__(self, *args, **kwargs):
        #if len(kwargs) > 0:
        #    dice_list = kwargs.pop('chooseabledice')
        #else:
        choice_list = [Wood, Stone, Gold, Land, Iron]
        given_list = [Wood, Wood, Stone, Stone, Gold]
        super(ChooseDiceForm, self).__init__(*args, **kwargs)
        number_choice_die = 3
        for x in range(1, number_choice_die+1):
            self.fields['choice_die'+str(x)] = forms.ChoiceField(
                label="Choice Die #"+str(x),
                widget=RadioImgWidget(),
                choices=self.make_choices(choice_list)
            )
        self.fields['given_dice'].choices = self.make_choices(given_list)


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
