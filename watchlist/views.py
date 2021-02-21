from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from bs4 import BeautifulSoup
import requests

from .models import Movie
from .forms import NewMovieForm, UpdateMovieForm

def index(request):
    ranked_list = Movie.objects.filter(watch_state="WD").order_by('-rating')
    to_watch_list = Movie.objects.filter(watch_state="TW")
    context = {'ranked_list': ranked_list, 'to_watch_list': to_watch_list}
    return render(request, 'watchlist/index.html', context)

def detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)

    if request.method == 'POST':
        movie = get_object_or_404(Movie, pk=movie_id)

        form = UpdateMovieForm(request.POST, movie)
        if form.is_valid():
            movie.watch_state = form.cleaned_data['new_watch_state']
            if form.cleaned_data['new_rating'] != None:
                movie.rating = form.cleaned_data['new_rating']

            movie.save()
            return HttpResponseRedirect("/watchlist/")
    else:
        form = UpdateMovieForm(request.POST, movie)


    return render(request, 'watchlist/detail.html', {'movie': movie, 'form': form})


def find_movie_page(title):
    '''Returns the html for the movie's IMDB page'''
    search_url = 'https://www.imdb.com/find?q=' + title.replace(' ', '+')
    search_page = requests.get(search_url)
    soup = BeautifulSoup(search_page.content, 'html.parser')

    movie_url = "https://www.imdb.com" + str(soup.find_all('td', class_='result_text')[0].a['href'])
    movie_page = requests.get(movie_url)
    return BeautifulSoup(movie_page.content, 'html.parser')


def new_movie(request):
    if request.method == 'POST':
        form = NewMovieForm(request.POST)
        if form.is_valid():
            newmov = Movie()
            newmov.movie_title = form.cleaned_data['movie_title']
            soup = find_movie_page(newmov.movie_title)
            newmov.synopsis = soup.find_all('div', class_='summary_text')[0].get_text()

            newmov.save()
            return HttpResponseRedirect("/watchlist/")
    else:
        form = NewMovieForm()

    return render(request, 'watchlist/newmovie.html', {'form': form})
