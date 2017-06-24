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
        if(not isinstance(user,User) ):
            raise Exception("Can't add this user")
        #TODO добавить в базу данных
        self.partic.append(user)

    def exclude_partic(self,user):
        if (not isinstance(user, User)):
            raise Exception("Can't add this user")
        #TODO убрать из базы данных
        self.partic.remove(user)


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
