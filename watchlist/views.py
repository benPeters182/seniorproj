from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from bs4 import BeautifulSoup
import requests

from .models import Movie, WatchList
from .forms import NewMovieForm, UpdateMovieForm, NewMovieOptionsForm

def index(request, list_name):
    watchlst = get_object_or_404(WatchList, name=list_name)
    wl_movies = Movie.objects.filter(list=watchlst)
    ranked_list = wl_movies.filter(watch_state="WD").order_by('-rating')
    to_watch_list = wl_movies.filter(watch_state="TW")
    lists = []
    for list in WatchList.objects.all():
        if list.name != list_name:
            lists.append(list)

    context = {'watchlst': watchlst,
                'lists': lists,
                'ranked_list': ranked_list,
                'to_watch_list': to_watch_list
    }
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

            if str(form.cleaned_data['delete_movie']) == 'delete':
                movie.delete()

            return HttpResponseRedirect("/watchlist/" + movie.list.name)
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


def new_movie(request, list_name):
    watchlst = get_object_or_404(WatchList, name = list_name)

    if request.method == 'POST':
        form = NewMovieForm(request.POST)
        if form.is_valid():
            movie_title = form.cleaned_data['movie_title']

            return HttpResponseRedirect("/watchlist/" + watchlst.name + "/options/Herbie")#"/watchlist/" + watchlst.name + "/new-movie-options/" + "Herbie")
    else:
        form = NewMovieForm()

    return render(request, 'watchlist/newmovie.html', {'watchlst': watchlst, 'form': form})

def new_movie_options(request, list_name, search_text):
    watchlst = get_object_or_404(WatchList, name = list_name)
    choices = [("https://www.imdb.com/title/tt0087469/?ref_=fn_al_tt_2", "Fortnite"), ("https://www.imdb.com/title/tt0087469/?ref_=fn_al_tt_2", "Different Limitless")]

    if request.method == 'POST':
        form = NewMovieOptionsForm(request.POST, movie_choices = choices)
        print("got to line 82")
        if form.is_valid():

            newmov = Movie()
            newmov.movie_title = form.cleaned_data['movie_title']
            soup = find_movie_page(newmov.movie_title)

            newmov.movie_title = soup.find('div', class_='title_wrapper').h1.get_text()
            newmov.synopsis = soup.find_all('div', class_='summary_text')[0].get_text()
            newmov.featured_img = soup.find('div', class_='poster').img['src']
            newmov.list = watchlst

            newmov.save()

            return HttpResponseRedirect("/watchlist/" + watchlst.name)
    else:
        form = NewMovieOptionsForm(movie_choices = choices)

    return render(request, 'watchlist/newmovieoptions.html', {'watchlst': watchlst, 'form': form, 'search_text': search_text})
