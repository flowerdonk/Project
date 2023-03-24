from django import forms
from .models import Movie

class MovieForm(forms.ModelForm):
    genre = forms.ChoiceField(
        choices=[('선택', 'None'), ('Comedy', 'Comedy'), ('Thriller', 'Thriller'), ('Romance', 'Romance')], 
    )

    score = forms.FloatField(
        min_value= 0,
        max_value= 5,
        widget= forms.NumberInput(
            attrs={
                'step' : 0.5,
            }
        )
    )
    release_date = forms.DateField(
        widget= forms.DateInput(
            attrs={
                'type':'date',
            }
        ),
    )
    class Meta:
        model = Movie
        fields = '__all__'
