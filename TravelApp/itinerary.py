import requests
from bs4 import BeautifulSoup
import random
import math
import twitter

def gen_it(data, senti, days):
    num_places = days*3
    time = ["Morning", "Afternoon", "Evening"]
    places = []
    price = []
    sent = []
    for key in senti:
        places.append(key[0])
    if num_places < len(data):
        places = places[:num_places]
    for p in places:
        price.append(data[p])
        for k,v in senti:
            if k==p:
                sent.append(v)

    out = []
    for i in range(0, len(places)):
        out.append((time[i%3], places[i], price[i], sent[i]))
    return out


def get_places(term, days):
    data = {}
    senti = {}
    url = "https://www.fabhotels.com/blog/places-to-visit-in-{}/".format(term)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for i in soup.find_all('h3'):
        if i.text[0] is "T":
            break
        senti[i.text] = twitter.getSentiments(i.text.split('.')[1])
        data[i.text] = int(math.ceil(random.randint(30,300) / 10)) * 10
    senti = sorted(senti.items(), key = lambda kv:(kv[1]), reverse=True)
    return gen_it(data, senti, days)


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

