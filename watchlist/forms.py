from django import forms


class NewMovieForm(forms.Form):
    movie_title = forms.CharField(label='Movie title', max_length=100)

class NewMovieOptionsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        movie_choices = kwargs.pop('movie_choices')
        super(NewMovieOptionsForm, self).__init__(*args, **kwargs)
        self.fields['movie_url'].choices = movie_choices

    movie_url = forms.ChoiceField(
        label='Which one is it?',
        required = False
    )


class UpdateMovieForm(forms.Form):

    new_rating = forms.DecimalField(
        label = 'Rating',
        required = False,
    )

    new_watch_state = forms.ChoiceField(
        label='Seen it?',
        choices = [('TW', 'To watch'), ('WD', 'Watched')],
        required = False
    )

    delete_movie = forms.CharField(
        label='Type "delete" to delete',
        max_length=6,
        required = False
    )
