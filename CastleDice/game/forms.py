from django import forms
from django.forms import widgets


class ChooseGameForm(forms.Form):
    game_choice = forms.ChoiceField(
        label="New or existing Game?",
        widget=widgets.RadioSelect(),
        choices=(
            ("solo", "New Solo Game"),
            ("new", "New Game"),
            ("id", "Continue Game"),
        ),
    )
    game_id = forms.CharField(label="Continue Game by id", required=False)
