from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from bs4 import BeautifulSoup
import requests

from .models import Movie, WatchList, Show
from .forms import NewMovieForm, UpdateMovieForm, UpdateShowForm, NewMovieOptionsForm
from datetime import date

def movie_index(request, list_name):
    watchlst = get_object_or_404(WatchList, name=list_name)
    wl_movies = Movie.objects.filter(list=watchlst)
    ranked_list = wl_movies.filter(watch_state="WD").order_by('-rating')
    chronological_list = wl_movies.filter(watch_state="WD").order_by('watch_date')
    to_watch_queued = wl_movies.filter(watch_state="TW").filter(queued=True)
    to_watch_list = wl_movies.filter(watch_state="TW").filter(queued=False)
    lists = []
    for list in WatchList.objects.all():
        if list.name != list_name:
            lists.append(list)

    context = {'watchlst': watchlst,
                'lists': lists,
                'ranked_list': ranked_list,
                'chronological_list': chronological_list,
                'to_watch_queued': to_watch_queued,
                'to_watch_list': to_watch_list
    }
    return render(request, 'watchlist/movie_index.html', context)

def show_index(request, list_name):
    watchlst = get_object_or_404(WatchList, name=list_name)
    wl_shows = Show.objects.filter(list=watchlst)
    ranked_list = wl_shows.filter(watch_state="WD").order_by('-rating')
    chronological_list = wl_shows.filter(watch_state="WD").order_by('-finish_date')

    to_watch_list = wl_shows.filter(watch_state="TW")
    watching_list_queued = wl_shows.filter(watch_state="WG").filter(queued=True)
    watching_list = wl_shows.filter(watch_state="WG").filter(queued=False)
    to_watch_queued = wl_shows.filter(watch_state="TW").filter(queued=True)
    to_watch_list = wl_shows.filter(watch_state="TW").filter(queued=False)
    lists = []
    for list in WatchList.objects.all():
        if list.name != list_name:
            lists.append(list)

    context = {'watchlst': watchlst,
                'lists': lists,
                'ranked_list': ranked_list,
                'chronological_list': chronological_list,
                'watching_list_queued': watching_list_queued,
                'watching_list': watching_list,
                'to_watch_queued': to_watch_queued,
                'to_watch_list': to_watch_list
    }
    return render(request, 'watchlist/show_index.html', context)

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    print(movie.watch_date)
    if request.method == 'POST':
        movie = get_object_or_404(Movie, pk=movie_id)

        form = UpdateMovieForm(request.POST)
        if form.is_valid():
            if movie.watch_state != 'WD' and form.cleaned_data['new_watch_state'] == 'WD':
                movie.watch_date = date.today().strftime("%Y-%m-%d")

            movie.watch_state = form.cleaned_data['new_watch_state']
            if form.cleaned_data['new_rating'] != None:
                movie.rating = form.cleaned_data['new_rating']
            movie.queued = form.cleaned_data['queued']
            movie.save()

            if str(form.cleaned_data['delete_movie']) == 'delete':
                movie.delete()

            return HttpResponseRedirect("/watchlist/" + movie.list.name + "/movies")
    else:
        form = UpdateMovieForm(request.POST, movie)

    return render(request, 'watchlist/movie-detail.html', {'movie': movie, 'form': form})

def show_detail(request, show_id):
    show = get_object_or_404(Show, pk=show_id)

    if request.method == 'POST':
        sform = UpdateShowForm(request.POST)
        if sform.is_valid():
            if show.watch_state == 'TW' and sform.cleaned_data['new_watch_state'] == 'WG':
                show.start_date = date.today().strftime("%Y-%m-%d")
            if show.watch_state != 'WD' and sform.cleaned_data['new_watch_state'] == 'WD':
                show.finish_date = date.today()

            show.watch_state = sform.cleaned_data['new_watch_state']
            if sform.cleaned_data['new_rating'] != None:
                show.rating = sform.cleaned_data['new_rating']
            show.queued = sform.cleaned_data['queued']
            show.save()

            if str(sform.cleaned_data['delete_show']) == 'delete':
                show.delete()

            return HttpResponseRedirect("/watchlist/" + show.list.name + "/shows")
    else:
        form = UpdateShowForm(request.POST, show)

    return render(request, 'watchlist/show-detail.html', {'show': show, 'form': form})


def find_movie_page(title):
    '''Returns the html for the movie's IMDB page'''
    search_url = 'https://www.imdb.com/find?q=' + title.replace(' ', '+') + '&s=tt&ttype=ft&ref_=fn_ft'
    search_page = requests.get(search_url)
    soup = BeautifulSoup(search_page.content, 'html.parser')

    movie_url = "https://www.imdb.com" + str(soup.find_all('td', class_='result_text')[0].a['href'])
    movie_page = requests.get(movie_url)
    return BeautifulSoup(movie_page.content, 'html.parser')


def find_choices(title, show_or_movie):
    '''Returns list of tuples for choice field'''
    search_url = 'https://www.imdb.com/find?q=' + title.replace(' ', '+') + '&s=tt&ttype='

    if show_or_movie == "movie":
        search_url = search_url + 'ft&ref_=fn_ft'
    elif show_or_movie == "show":
        search_url = search_url + 'tv&ref_=fn_tv'

    search_page = requests.get(search_url)
    soup = BeautifulSoup(search_page.content, 'html.parser')

    num_possible_movies = len(soup.find_all('td', class_='result_text'))
    MAX_MOVIE_OPTIONS = 10
    if num_possible_movies >= MAX_MOVIE_OPTIONS:
        num_possible_movies = MAX_MOVIE_OPTIONS

    choices=[]
    for i in range(num_possible_movies):
        url = 'https://www.imdb.com' + str(soup.find_all('td', class_='result_text')[i].a['href'])
        title = soup.find_all('td', class_='result_text')[i].get_text().strip()
        choices.append((url , title))

    return choices


def new_movie(request, list_name):
    watchlst = get_object_or_404(WatchList, name = list_name)

    if request.method == 'POST':
        form = NewMovieForm(request.POST)
        if form.is_valid():
            movie_title = form.cleaned_data['movie_title']

            return HttpResponseRedirect("/watchlist/" + watchlst.name + "/options/Herbie")
    else:
        form = NewMovieForm()

    return render(request, 'watchlist/newmovie.html', {'watchlst': watchlst, 'form': form})


def new_movie_options(request, list_name, search_text):
    watchlst = get_object_or_404(WatchList, name = list_name)
    choices = find_choices(search_text, "movie")

    if request.method == 'POST':
        form = NewMovieOptionsForm(request.POST, movie_choices = choices)
        print("got to line 82")
        if form.is_valid():

            newmov = Movie()
            url = form.cleaned_data['movie_url']
            movie_page = requests.get(url)
            soup = BeautifulSoup(movie_page.content, 'html.parser')

            newmov.movie_title = soup.find('div', class_='title_wrapper').h1.get_text()
            newmov.synopsis = soup.find_all('div', class_='summary_text')[0].get_text()
            newmov.featured_img = soup.find('div', class_='poster').img['src']
            newmov.list = watchlst

            newmov.save()

            return HttpResponseRedirect("/watchlist/" + watchlst.name + "/movies")
    else:
        form = NewMovieOptionsForm(movie_choices = choices)

    return render(request, 'watchlist/newmovieoptions.html', {'watchlst': watchlst, 'form': form, 'search_text': search_text})

def new_show_options(request, list_name, search_text):
    watchlst = get_object_or_404(WatchList, name = list_name)
    choices = find_choices(search_text, "show")

    if request.method == 'POST':
        form = NewMovieOptionsForm(request.POST, movie_choices = choices)
        print("got to line 82")
        if form.is_valid():

            newshow = Show()
            url = form.cleaned_data['movie_url']
            show_page = requests.get(url)
            soup = BeautifulSoup(show_page.content, 'html.parser')

            newshow.show_title = soup.find('div', class_='title_wrapper').h1.get_text()
            newshow.synopsis = soup.find_all('div', class_='summary_text')[0].get_text()
            newshow.featured_img = soup.find('div', class_='poster').img['src']
            newshow.list = watchlst

            newshow.save()

            return HttpResponseRedirect("/watchlist/" + watchlst.name + "/shows")
    else:
        form = NewMovieOptionsForm(movie_choices = choices)

    return render(request, 'watchlist/newshowoptions.html', {'watchlst': watchlst, 'form': form, 'search_text': search_text})
