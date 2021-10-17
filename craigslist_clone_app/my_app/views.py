from typing import Text, final
import requests
from requests.compat import quote_plus
from django.shortcuts import render
from bs4 import BeautifulSoup
from . import models
# Create your views here.

BASE_CRAIGSLIST_URL = 'https://losangeles.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'


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

    # post_titles = post_listings[0].find(class_='result-title').text
    # post_url = post_listings[0].find('a').get('href')
    # post_price = post_listings[0].find(class_='result-price')
    # OPTIONAL PART FOR EMPTY PRICES----------------------------------
    # if post_price == None:
    #     post_price = 'Price Unspecified'

    final_postings = []
    for post in post_listings:
        post_titles = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price')
        else:
            post_price = 'N/A'

        if post.find(class_='result-image',).get('data-ids'):
            post_image_url = post.find(
                class_='result-image',).get('data-ids').split(',')[0].split(':')[1]
            print(post_image_url)
            post_image_url = BASE_IMAGE_URL.format(post)

        final_postings.append((post_titles, post_url, post_price))

    stuff_for_frontend = {'search': search, 'final_postings': final_postings}
    # print(data)
    return render(request, 'my_app/new_search.html', stuff_for_frontend)
