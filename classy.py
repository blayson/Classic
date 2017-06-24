import requests
import arrow
from datetime import datetime


class User:
    def __init__(self,name="Lecha",surname='Ermak',age=20,foto_path="/home/andrei/Загрузки/1.jpg",
                 kontakt_ref="https://www.facebook.com/profile.php?id=100010513029228&fref=hovercard&hc_location=chat"):
        # self.id = id
        self.name = name        #имя пользователя
        self.surname = surname  #фамилия пользователя
        self.age = age          #возраст пользователя
        self.foto_path = foto_path          #путь к фото
        self.kontakt_path = kontakt_ref     #ссылка на профиль(FB, VK ...)

    def create_trip(self,dest,date,time,time_diff=3600,max_cap = 20):
        trip = Trip(dest,dest,date,time,time_diff,max_cap)
        trip.add_partic(self)
        return trip


class Trip:
    def __init__(self, dest,date,time,time_diff=3600,max_cap = 20):
        # self.id = id
        self.dest = dest    #аэропорт
        self.date = date    #дата приезда на место встречи
        self.time = time    #время приезда на место встречи
        self.time_diff = time_diff   #время в секундах которое эта группа может подождать
        self.max_cap = max_cap       #максимальное количество людей в путешествии
        self.partic = []             #список всех участников

    def add_partic(self,user):
        if not isinstance(user, User):
            raise Exception("Can't add this user")
        #TODO добавить в базу данных
        self.partic.append(user)

    def exclude_partic(self,user):
        if not isinstance(user, User):
            raise Exception("Can't add this user")
        #TODO убрать из базы данных
        self.partic.remove(user)

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
        time_diff = self.time_diff * 2
        for flight in response['data']:
            if time_to:
                user_dt = arrow.get('{} {}'.format(date_to, time_to), 'DD/MM/YYYY HH:mm')
                flight_dt_max = user_dt.timestamp + time_diff
                flight_dt_min = user_dt.timestamp - time_diff
                if (int(flight['aTimeUTC']) > flight_dt_min) and (int(flight['aTimeUTC']) < flight_dt_max):
                    fo = Flight(from_tmsp=flight['dTimeUTC'], to_tmsp=flight['aTimeUTC'], cost=flight['price'],
                                duration=flight['fly_duration'], from_location=(flight['cityFrom'], flight['flyFrom']),
                                book_url=flight['deep_link'])
                    data.append(fo)
            else:
                if arrow.get(flight['aTimeUTC']).format('DD/MM/YYYY') == arrow.get(date_to, 'DD/MM/YYYY').format(
                        'DD/MM/YYYY'):
                    fo = Flight(from_tmsp=flight['dTimeUTC'], to_tmsp=flight['aTimeUTC'], cost=flight['price'],
                                duration=flight['fly_duration'], from_location=(flight['cityFrom'], flight['flyFrom']),
                                book_url=flight['deep_link'])
                    data.append(fo)
        return data

    def to_dict(self, data):
        data_list = []
        data_dict = {}

        for item in data:
            data_dict['from_tmsp'] = datetime.utcfromtimestamp(item.from_tmsp)
            data_dict['to_tmsp'] = datetime.utcfromtimestamp(item.to_tmsp)
            data_dict['cost'] = item.cost
            data_dict['duration'] = item.duration
            data_dict['from_location'] = item.from_location
            data_dict['book_url'] = item.book_url
            data_dict['dest'] = self.dest
            data_list.append(data_dict)
        return data_list


class Flight:
    def __init__(self,from_tmsp,to_tmsp,cost,duration,from_location,book_url):
        # self.id = id
        self.from_tmsp = from_tmsp  #временной штамп отлёта
        self.to_tmsp = to_tmsp      #временной штамп прилёта
        self.cost = cost            #цена перелёта
        self.duration = duration    #длительность перелёта
        self.book_url = book_url        #ссылка на бронь билета
        #TODO inicialization with sygic
        self.from_location = from_location  #кортеж (город, аэропорт)
