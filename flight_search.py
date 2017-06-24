import requests
import arrow
import dateutil.parser
from datetime import datetime
import time

from classy import Flight


class Trip:
    def __init__(self, dest, date,time,time_diff=3600,max_cap = 20):
        # self.id = id
        self.dest = dest
        self.date = date
        self.time = time
        self.time_diff = time_diff
        self.max_cap = max_cap
        self.partic = []

    def find_flights(self, fly_to, date_to, fly_from, time_to=None):
        api_url = 'https://api.skypicker.com/flights'

        adt = arrow.get(date_to, 'DD/MM/YYYY')
        date_from = adt.shift(days=-1).format('DD/MM/YYYY')
        print(date_from, date_to)

        params = {
            'flyFrom': fly_from,
            'to': fly_to,
            'dateFrom': date_from,
            'dateTo': date_to,
            'partner': 'picky',
            'typeFlight': 'oneway',
        }
        response = requests.get(api_url, params=params).json()

        data = []

        for flight in response['data']:
            if time_to:
                user_dt = arrow.get('{} {}'.format(date_to, time_to), 'DD/MM/YYYY HH:mm')
                time_diff = self.time_diff * 2
                flight_dt_max = user_dt.timestamp + time_diff
                flight_dt_min = user_dt.timestamp - time_diff
                if (int(flight['aTimeUTC']) > flight_dt_min) and (int(flight['aTimeUTC']) < flight_dt_max):
                    fo = Flight(from_tmsp=flight['dTimeUTC'], to_tmsp=flight['aTimeUTC'], cost=flight['price'],
                                duration=flight['fly_duration'], from_location=(flight['cityFrom'], flight['flyFrom']))
                    data.append(fo)
            else:
                if arrow.get(flight['aTimeUTC']).format('DD/MM/YYYY') == arrow.get(date_to, 'DD/MM/YYYY').format('DD/MM/YYYY'):
                    fo = Flight(from_tmsp=flight['dTimeUTC'], to_tmsp=flight['aTimeUTC'], cost=flight['price'],
                                duration=flight['fly_duration'], from_location=(flight['cityFrom'], flight['flyFrom']))
                    data.append(fo)
        return data

if __name__ == '__main__':

    t = Trip(1, 2, 3)
    r = t.find_flights(fly_from='PRG', fly_to='LGW',
                       date_to=arrow.utcnow().shift(days=+1).format('DD/MM/YYYY'), time_to='15:10')
    for item in r:
        print(item.cost)
        print(item.from_location)
        print(datetime.utcfromtimestamp(item.from_tmsp), datetime.utcfromtimestamp(item.to_tmsp))
