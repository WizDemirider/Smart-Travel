import requests
from bs4 import BeautifulSoup
import random
import math

def gen_it(data, days):
    num_places = days*3
    time = ["Between 8 and noon", "Post noon", "Evening or night"]
    places = []
    price = []
    for key in data.keys():
        places.append(key)
    if num_places > len(data):
        places[:num_places]
    for p in places:
        price.append(data[p])

    print("Time\tPlace\tPrice")
    for i in range(0, num_places):
        print(str(time[i%3]) + "\t" + str(places[i]) + "\t" + str(price[i]))


def get_places(term, days):
    data = {}
    url = "https://www.fabhotels.com/blog/places-to-visit-in-{}/".format(term)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for i in soup.find_all('h3'):
        if i.text[0] is "T":
            break
        data[i.text] = int(math.ceil(random.randint(30,300) / 10)) * 10

    gen_it(data, days)


def get_it(term, days):
    if term != "pune" and term != "delhi" and term != "kolkata":
        get_places(term, days)
    else:
        url = 'https://www.fabhotels.com/blog/2-days-{}-itinerary/'.format(term)

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.find('table')
        if table is not None:
            table_rows = table.find_all('tr')
            for tr in table_rows:
                td = tr.find_all('td')
                row = [i.text for i in td]
                print(row)
        else:
            print("Nope")

get_places("mumbai", 3)