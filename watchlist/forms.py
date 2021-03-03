from django import forms


class NewMovieForm(forms.Form):
    movie_title = forms.CharField(label='Movie title', max_length=100)

class NewMovieOptionsForm(forms.Form):

    def __init__(self, movie_choices):

        self.fields['movie_url'].choices = [("https://www.imdb.com/title/tt0087469/?ref_=fn_al_tt_2", "Limitless (I) (2011)"), ("https://www.imdb.com/title/tt0087469/?ref_=fn_al_tt_2", "Different Limitless")]

    movie_url = forms.ChoiceField(
        label='Which one is it?',
        choices = [("https://www.imdb.com/title/tt0087469/?ref_=fn_al_tt_2", "Limitless (I) (2011)"), ("https://www.imdb.com/title/tt0087469/?ref_=fn_al_tt_2", "Different Limitless")],
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
