from bs4 import BeautifulSoup
import requests

from .models import Movie, WatchList, Show, Role, Actor

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

def add_roles(title):
    '''creates Actors and Roles given a Show or Movie'''
    title_page = requests.get(str(title.url) + "fullcredits?ref_=tt_cl_sm#cast")
    soup = BeautifulSoup(title_page.content, 'html.parser')
    cast_list = soup.find_all('table', class_='cast_list')
    count = 0
    MAX_ROLES = 30
    rows = cast_list[0].find_all("tr")
    for row in rows:
        if len(row.find_all("td")) >= 2:
            actor_url = "https://www.imdb.com/" + row.find_all("td")[1].a['href']
            role_name = row.find_all("td")[3].a.get_text()
            add_role(title, actor_url, role_name)
            count+=1
            if count > MAX_ROLES:
                break


def add_role(title, actor_url, role_name):
    '''Helper for add_roles'''
    if isinstance(title, Movie):
        title_type = "movie"
    elif isinstance(title, Show):
        title_type = "show"
    else:
        raise Exception("title must be Show or Movie object")

    new_role = Role()
    new_role.name = role_name

    if title_type == "movie":
        new_role.movie = title
    else:
        new_role.show = title

    if title.watch_state != "TW":
        new_role.seen = True

    actor_id = actor_url[29:36]
    if Actor.objects.filter(imdb_id = actor_id, list = title.list).exists() == 0:
        add_actor(actor_url, title.list)

    new_role.actor = Actor.objects.get(imdb_id = actor_id, list = title.list)
    new_role.save()
    print("Role: " + str(new_role))


def add_actor(actor_url, list):
    '''helper for add_role'''
    actor_page = requests.get(actor_url)
    soup = BeautifulSoup(actor_page.content, 'html.parser')

    new_actor = Actor()
    new_actor.imdb_id = actor_url[29:36]
    new_actor.list = list
    new_actor.name = soup.find_all('h1', class_='header')[0].get_text().strip()
    print("Actor: " + str(new_actor))
    new_actor.save()
