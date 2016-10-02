from django import forms
from django.forms import widgets

from common.dice import DICE_COUNT
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
                        '<label{0}><input{1} /> <img class="die {2} {3}_{4} mid"></label>',
                        label_for, flatatt(final_attrs), option_value,
                        die_face[0], die_face[1])
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
                    '<label{0}><input{1} /> <img class="die {2} mid"></label>',
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
        choice_list = DICE_COUNT.keys()
        given_dict = initial['given_dice']
        no_choices = initial['no_choices']
        for x in range(1, no_choices+1):
            self.fields['choice_die'+str(x)] = forms.ChoiceField(
                label="Choice Die #"+str(x),
                widget=RadioImgWidget(),
                choices=self.make_choices(choice_list)
            )
        self.fields['given_dice'].choices = \
            self.make_choices_from_dict(given_dict)

    def make_choices_from_dict(self, die_count_dict):
        d_list = [
            key for key, value in die_count_dict.iteritems()
            for i in range(0, value)
        ]

        return self.make_choices(d_list)

    # preps the form choices for user
    @staticmethod
    def make_choices(d_list):
        d_choices = []
        for die in d_list:
            if die in DICE_COUNT.keys():
                d_choices.append((die, die))
        return d_choices


class GatherDiceForm(forms.Form):
    dice_pool = forms.ChoiceField(
        label="Gather Your Die",
        widget=RadioImgWidget()
    )

    def __init__(self, *args, **kwargs):
        super(GatherDiceForm, self).__init__(*args, **kwargs)
        game_obj = Game.objects.get(id=kwargs['initial']['game_id'])

        self.fields['dice_pool'].choices = tuple(
            ("{resource} {face}_{count}".format(
                resource=resource,
                face=die_face_tuple[0],
                count=die_face_tuple[1]),
             "{count} {face}".format(
                 count=die_face_tuple[1],
                 face=die_face_tuple[0].capitalize())
            )
            for resource, dice_face_list in game_obj.gather_dice.items()
            for die_face_tuple in dice_face_list
        )

        # self.fields['dice_pool'].choices = [
        #     [k, l] for k, l in game_obj.world_pool.items()
        # ]
