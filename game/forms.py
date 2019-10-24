from django import forms
from game.models import Game


class MakeNumber(forms.ModelForm):
    guessed_number = forms.IntegerField(label='Загадайте число:')

    class Meta(object):
        model = Game
        exclude = ('player', 'active')


class CheckNumber(forms.Form):
    number = forms.IntegerField(label='Проверьте число:')