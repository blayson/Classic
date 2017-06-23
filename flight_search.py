import requests
from classy import Flight


def find_flight(fly_from, fly_to, date_from, date_to):
    api_url = 'https://api.skypicker.com/flights'

    params = {
        'flyFrom': fly_from,
        'to': fly_to,
        'dateFrom': date_from,
        'dateTo': date_to,
        'partner': 'picky',
        'typeFlight': 'oneway',
    }
    response = requests.get(api_url, params=params)

    f = Flight(id,from_tmsp,to_tmsp,cost,duration,from_location)