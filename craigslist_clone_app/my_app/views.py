from typing import final
import requests
from requests.compat import quote_plus
from bs4 import BeautifulSoup
from django.shortcuts import render
# Create your views here.

BASE_CRAIGSLIST_URL = 'https://indore.craigslist.org/d/housing/search/hhh?query={}'


def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    # print(final_url)
    response = requests.get(final_url)
    stuff_for_frontend = {'search': search, }
    data = response.text
    # print(data)
    return render(request, 'my_app/new_search.html', stuff_for_frontend)
