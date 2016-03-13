from django import forms
from django.forms import widgets
from CD_globals import TURN, DICE_COUNT, WOOD, STONE, GOLD, LAND, IRON
from game.models import Game
# I want to remove the above resources as LISTED things.
# should not need to know, ever

from itertools import chain
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.forms.util import flatatt


class CheckboxMultipleImgWidget(widgets.CheckboxSelectMultiple):

    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        output = []
        # Normalize to strings
        str_values = set([force_text(v) for v in value])
        first = True
        for i, (option_value, option_label) in \
                enumerate(chain(self.choices, choices)):
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                label_for = format_html(' for="{0}"', final_attrs['id'])
            else:
                label_for = ''
            cb = widgets.CheckboxInput(

                final_attrs,
                check_test=lambda value: value in str_values
            )
            option_value = force_text(option_value)
            rendered_cb = cb.render(name, option_value)
            option_label = force_text(option_label)
            output.append(format_html(
                '<label{0}>{1} <img class="die {2} mid"></label>',
                label_for, rendered_cb, option_label
            ))
        output.append("<br>")
        return mark_safe('\n'.join(output))


class RadioImgWidget(widgets.RadioSelect):
    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name, type="radio")

        output = []
        for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if type(option_label) is list:
                for j, die_face in enumerate(option_label):
                    if has_id:
                        final_attrs = dict(final_attrs, id='%s_%s_%s' % (attrs['id'], i, j))
                        label_for = format_html(' for="{0}"', final_attrs['id'])
                    else:
                        label_for = ''
                    if not (type(option_value) is bool or
                            not option_value or value == ''):
                        # Only add the 'value' attribute if a value is non-empty.
                        final_attrs['value'] = force_text(
                            unicode(str(option_value) + "_" + str(die_face[0])
                            + "_" + str(die_face[1]), "utf-8")
                        )
                    die_face[0] = force_text(die_face[0])
                    output.append(format_html(
                        '<label{0}><input{1} /> <img class="die_{2} {3}x{4} mid"> {5}</label><br>',
                        label_for, flatatt(final_attrs), option_value,
                        die_face[0], die_face[1], die_face[0].capitalize())
                    )
            else:
                # ('wood', 'wood')
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
                output.append(format_html(
                    '<label{0}><input{1} /> <img class="die {2} mid"> {3}</label><br>',
                    label_for, flatatt(final_attrs), option_value,
                    option_label)
                )

        return mark_safe('\n'.join(output))

    # def make_labe_and_input(self, option_value, option_label):


class ChooseDiceForm(forms.Form):
    given_dice = forms.MultipleChoiceField(
        label="Given Dice",
        widget=CheckboxMultipleImgWidget({
            'style': "display:none",
            "checked": "checked"
        })
    )

    def __init__(self, *args, **kwargs):
        super(ChooseDiceForm, self).__init__(*args, **kwargs)
        initial = kwargs.pop('initial')
        if 'turn_no' in initial:
            turn_no = initial['turn_no']
        else:
            turn_no = 00
        choice_list = [WOOD, STONE, GOLD, LAND, IRON]
        given_list = TURN[turn_no]['given_dice']
        no_choices = TURN[turn_no]['no_choices']
        for x in range(1, no_choices+1):
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
            if die == WOOD:
                d_choices.append((WOOD, WOOD))
            elif die == STONE:
                d_choices.append((STONE, STONE))
            elif die == GOLD:
                d_choices.append((GOLD, GOLD))
            elif die == LAND:
                d_choices.append((LAND, LAND))
            elif die == IRON:
                d_choices.append((IRON, IRON))
        return d_choices


class GatherDiceForm(forms.Form):
    dice_pool = forms.ChoiceField(
        label="Gather Your Die",
        widget=RadioImgWidget()
    )

    def __init__(self, *args, **kwargs):
        super(GatherDiceForm, self).__init__(*args, **kwargs)
        game_obj = Game.objects.get(pk=kwargs['initial']['game_id'])

        self.fields['dice_pool'].choices = tuple(
            (str(str(k) + "_" + str(t[0]) + "_" + str(t[1])),
             str(str(t[1])+ " " + str(t[0]).capitalize()))
            for k, l in game_obj.world_pool.items()
            for t in l
        )

        # self.fields['dice_pool'].choices = [
        #     [k, l] for k, l in game_obj.world_pool.items()
        # ]
