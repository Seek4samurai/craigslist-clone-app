from typing import final
import requests
from requests.compat import quote_plus
from django.shortcuts import render
from bs4 import BeautifulSoup
from . import models
# Create your views here.

BASE_CRAIGSLIST_URL = 'https://indore.craigslist.org/search/?query={}'


def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    # print(final_url)
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    post_titles = soup.find_all('a', {'class': 'result-title'})
    print(post_titles)
    stuff_for_frontend = {'search': search, }
    # print(data)
    return render(request, 'my_app/new_search.html', stuff_for_frontend)
