from django import forms


class NewMovieForm(forms.Form):
    movie_title = forms.CharField(label='Movie title', max_length=100)

class UpdateMovieForm(forms.Form):

    new_rating = forms.DecimalField(
        label = 'Rating',
        required = False,
    )
    new_watch_state = forms.ChoiceField(
        label=' ',
        choices = [('TW', 'To watch'), ('WD', 'Watched')],
        required = False
    )
