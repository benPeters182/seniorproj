from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from bs4 import BeautifulSoup
import requests

from .models import Movie, WatchList, Show
from .forms import UpdateMovieForm, UpdateShowForm, NewMovieOptionsForm
from datetime import date
from .utils import *


#Index Views

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

def actor_index(request, list_name):
    watchlst = get_object_or_404(WatchList, name=list_name)

    actor_occurances = []   #accumulate list of actors that are in list more than once
                            #(actor, occurances)
    for actor in Actor.objects.filter(list=watchlst):
        n = len(Role.objects.filter(actor=actor))
        if n > 1:
            actor_occurances.append((actor, n))
        elif n == 0:
            actor.delete()

    actor_occurances.sort(reverse=True, key=lambda tup: tup[1])
    context = { 'watchlst': watchlst, 'actor_occurances': actor_occurances }

    return render(request, 'watchlist/actor-index.html', context)


#Detail Views

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
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

def actor_detail(request, actor_id):
    actor = get_object_or_404(Actor, pk=actor_id)
    roles = Role.objects.filter(actor=actor)

    context = { 'actor': actor, 'roles': roles}

    return render(request, 'watchlist/actor-detail.html', context)


#Cast Views

def movie_cast(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    title_roles = Role.objects.filter(movie=movie)
    context = {'title': movie, 'roles': title_roles, "title_type": Movie}

    return render(request, 'watchlist/cast-list.html', context)


def show_cast(request, show_id):
    show = get_object_or_404(Show, pk=show_id)
    title_roles = Role.objects.filter(show=show)
    context = {'title': show, 'roles': title_roles, "title_type": Show}

    return render(request, 'watchlist/cast-list.html', context)



#New Title Views

def new_movie_options(request, list_name, search_text):
    watchlst = get_object_or_404(WatchList, name = list_name)
    choices = find_choices(search_text, "movie")

    if request.method == 'POST':
        form = NewMovieOptionsForm(request.POST, movie_choices = choices)
        if form.is_valid():

            newmov = Movie()
            url = form.cleaned_data['movie_url']
            movie_page = requests.get(url)
            soup = BeautifulSoup(movie_page.content, 'html.parser')

            newmov.movie_title = soup.find('div', class_='title_wrapper').h1.get_text()
            newmov.synopsis = soup.find_all('div', class_='summary_text')[0].get_text()
            newmov.featured_img = soup.find('div', class_='poster').img['src']
            newmov.list = watchlst
            newmov.url = url

            newmov.save()

            add_roles(newmov)

            return HttpResponseRedirect("/watchlist/" + watchlst.name + "/movies")
    else:
        form = NewMovieOptionsForm(movie_choices = choices)

    return render(request, 'watchlist/newmovieoptions.html', {'watchlst': watchlst, 'form': form, 'search_text': search_text})


def new_show_options(request, list_name, search_text):
    watchlst = get_object_or_404(WatchList, name = list_name)
    choices = find_choices(search_text, "show")

    if request.method == 'POST':
        form = NewMovieOptionsForm(request.POST, movie_choices = choices)

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
