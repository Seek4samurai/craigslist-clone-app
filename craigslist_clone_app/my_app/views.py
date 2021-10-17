from typing import Text, final
import requests
from requests.compat import quote_plus
from django.shortcuts import render
from bs4 import BeautifulSoup
from . import models
# Create your views here.

BASE_CRAIGSLIST_URL = 'https://losangeles.craigslist.org/search/?query={}'


def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    post_listings = soup.find_all('li', {'class': 'result-row'})
    post_titles = post_listings[0].find(class_='result-title').text
    post_url = post_listings[0].find('a').get('href')
    post_price = post_listings[0].find(class_='result-price')
    # if post_price == None:
    #     post_price = 'Price Unspecified'
    print(post_titles)
    print(post_url)
    print(post_price)
    final_posting = []
    for post in post_listings:
        post_titles = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        post_price = post.find(class_='result-price')

    stuff_for_frontend = {'search': search, }
    # print(data)
    return render(request, 'my_app/new_search.html', stuff_for_frontend)
