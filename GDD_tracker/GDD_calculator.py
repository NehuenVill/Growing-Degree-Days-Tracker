import requests
import time
from datetime import datetime
from datetime import timedelta
from GDD_tracker.models import Dates

class GDD:
    
    def __init__(self, Pest, date, location):

        self.weather_loc = {

            "Amazonas": {"weather API" : "Amazonas", "NASA API" : "lat=-6.6014&lon=-58.3885"},
            "Bonanza": {"weather API" : "Guatemala,Escuintla", "NASA API" : "lat=14.090487&lon=-90.763009"},
            "Bouganvilia": {"weather API" : "Guatemala,Escuintla", "NASA API" : "lat=14.103545&lon=-90.933469"},
            "Cengicaña": {"weather API" : "Guatemala,Escuintla", "NASA API" : "lat=14.340186&lon=-91.058353"},
            "Costa Brava": {"weather API" : "Guatemala,Escuintla", "NASA API" : "lat=14.256015&lon=-90.881885"},
            "El Balsamo": {"weather API" : "Guatemala,Escuintla", "NASA API" : "lat=14.256015&lon=-90.881885"},
            "Escuintla Irlanda": {"weather API" : "Guatemala,Escuintla", "NASA API" : "lat=14.166821&lon=-91.428798"},
            "La Giralta": {"weather API" : "Guatemala,Escuintla", "NASA API" : "lat=14.256015&lon=-90.881885"},
            "Mazatenango San Nico": {"weather API" : "Guatemala,Suchitepequez", "NASA API" : "lat=14.211580&lon=-91.590868"},
            "Naranjales": {"weather API" : "Guatemala,Suchitepequez", "NASA API" : "lat=14.211580&lon=-91.590868"},
            "Petén oficina": {"weather API" : "Guatemala,Escuintla", "NASA API" : "lat=14.166821&lon=-91.428798"},
            "Puyumate": {"weather API" : "Guatemala,Escuintla", "NASA API" : "lat=14.166821&lon=-91.428798"},
            "Retalhuleu Xoluta": {"weather API" : "Guatemala,Retalhuleu", "NASA API" : "lat=14.4683&lon=-91.8447"},
            "San Antonio del Valle": {"weather API" : "Guatemala,Escuintla", "NASA API" : "lat=14.256015&lon=-90.881885"},
            "San Rafael": {"weather API" : "Guatemala,Santa+Rosa", "NASA API" : "lat=-14.036281&lon=-90.617136"},
            "Santa Rosa La candelaria": {"weather API" : "Guatemala,Santa+Rosa", "NASA API" : "lat=-14.036281&lon=-90.617136"},
            "Tehuantepeq": {"weather API" : "Guatemala,Escuintla", "NASA API" : "lat=14.256015&lon=-90.881885"}
        }

        self.pests = {
    
        "Armyworm":
        {
        "GT_max": 29,
        "GT_min": 10,
        "GT_base": 10,
        "stages": {
            "0" : {"warning" : "It's on the stage zero (0 - 71 GGDs), Eggs are growing", "range" : range(0, 71)},
            "1" : {"warning" : "It's on the first stage (71 - 205 GDDs), you'll see eggs appearing", "range": range(71, 205)},
            "2": {"warning" : "It's on the second stage (205 - 647 GDDs), you'll see larvae appearing", "range": range(205, 647)},
            "3": {"warning" : "It's on the third stage (from 647 GDDs), Adult moths will emerge", "range" : range(647, 1000000)}
        } 
        },

        "Cabbage Looper":
        {
        "GT_max": 32,
        "GT_min": 10,
        "GT_base": 10,
        "stages": {
            "0" : {"warning" : "It's on the stage zero (0 - 37 GGDs), Larvae are growing", "range" : range(0, 37)},
            "1" : {"warning" : "It's on the first stage (37 - 422 GDDs), you'll see larvae appearing", "range": range(37, 422)},
            "2": {"warning" : "It's on the second stage (from 422 GDDs), Adult moths will emerge", "range" : range(422, 1000000)}
        } 
        },

        "Corn Earworm":
        {
        "GT_max": 33,
        "GT_min": 12.6,
        "GT_base": 12.6,
        "stages": {
            "0" : {"warning" : "It's on the stage zero (0 - 104 GGDs), Larvae are growing", "range" : range(0, 104)},
            "1": {"warning" : "It's on the first stage (104 - 487 GDDs), you'll see larvae appearing", "range" : range(104, 487)},
            "2": {"warning" : "It's on the second stage (from 487 GDDs), Adult moths will emerge", "range" : range(487, 1000000)}
        } 
        },

        "San Jose Scale":
        {
        "GT_max": 32,
        "GT_min": 10.5,
        "GT_base": 10.5,
        "stages": {
            "0" : {"warning" : "It's on the stage zero (0 - 93 GGDs), Males are growing", "range" : range(0, 93)},
            "1": {"warning" : "It's on the first stage (93 - 523 GDDs), males will emerge", "range" : range(93, 523)},
            "2": {"warning" : "It's on the second stage (from 523 GDDs), females will emerge", "range" : range(523, 1000000)}
        } 
        },

        "Two Spotted Mite":
        {
        "GT_max": 1000,
        "GT_min": 12,
        "GT_base": 12,
        "stages": {
            "1" : {"warning" : "No info found!!", "range" : range(0, 10000000)}
        } 
        }

        }

        self.GTmax = self.pests[Pest]["GT_max"]
        self.GTmin = self.pests[Pest]["GT_min"]
        self.Tmax_today = 0
        self.Tmin_today = 0
        self.Tbase = self.pests[Pest]["GT_base"]
        self.GDD_TODAY = 0
        self.TOTAL_GDD = 0
        self.today = 0
        self.warnings = self.pests[Pest]["stages"]
        self.location = location 
        self.NASA_API = self.weather_loc[self.location]["NASA API"]
        self.Weather_API = self.weather_loc[self.location]["weather API"]
        self.pest = Pest
        self.get_today(date)

    def Request(self, day, case):

        if case:

            json_response = requests.get("http://api.weatherapi.com/v1/history.json?key=1177ed39630449ea9cd220345212104&q=%s&dt=%s" % (self.Weather_API, day)).json()

            temps = (json_response["forecast"]["forecastday"][0]["day"]["mintemp_c"], json_response["forecast"]["forecastday"][0]["day"]["maxtemp_c"])

            Temps = [round(temps[0]), round(temps[1])]

            return list(Temps) 

        else:

            Day = day.replace("-", "")

            json_response = requests.get("https://power.larc.nasa.gov/cgi-bin/v1/DataAccess.py?&request=execute&identifier=SinglePoint&parameters=T2M_MAX,T2M_MIN&startDate=%s&endDate=%s&userCommunity=SSE&tempAverage=DAILY&outputList=JSON&%s" % (Day, Day, self.NASA_API)).json()

            temps = (json_response["features"][0]["properties"]["parameter"]["T2M_MIN"]["%s" % (Day)], json_response["features"][0]["properties"]["parameter"]["T2M_MAX"]["%s" % (Day)])

            Temps = [round(temps[0]), round(temps[1])]

            return list(Temps)

    def TODAY(self):

        Today = datetime.now()
        self.today = datetime(Today.year, Today.month, Today.day)

    def get_today(self, date):

        self.TODAY()

        Delta_days = (self.today - date).days

        days = []

        for i in range(Delta_days + 1):

            days.append((date + timedelta(i)).strftime("%m-%d-%Y"))

        if date == self.today:

            days = []

        else:

            pass

        print(len(days))

        if len(days) > 2:

            self.previous_days(date, True)
            
        elif len(days) <= 2:

            if days[len(days)-2] == (self.today - timedelta(days=1)).strftime("%m-%d-%Y"):
                print("if")
                self.GDD_acumulated_today()

            elif days[len(days)-1] == self.today.strftime("%m-%d-%Y"):
                
                print("second elif")

                pass
            
        else:
            print("else")

            pass

    def previous_days(self, first_day, cond):

        self.TODAY()

        delta_days = self.today - first_day  

        if delta_days.days == 0:
            
            self.today = first_day

            self.today.strftime("%Y-%m-%d")

            temps = self.Request(self.today, True)

            self.Tmin_today = temps[0]
            self.Tmax_today = temps[1]

            self.GDD_TODAY_CALCULATOR()
            self.TOTAL_GDD += self.GDD_TODAY

            DATE = self.today
            T_MIN_CELSIUS = self.Tmin_today
            T_MAX_CELSIUS = self.Tmax_today
            GDD_TODAY = self.GDD_TODAY
            GDD_ACUMULATED = self.TOTAL_GDD

            D = Dates(Date=DATE, Pest= self.pest, Nearest_location= self.location, T_min_celsius=T_MIN_CELSIUS,  T_max_celsius=T_MAX_CELSIUS, GDD_Today=GDD_TODAY, GDD_Acumulated=GDD_ACUMULATED)

            D.save()

            time.sleep(0.7)

        else:

            if cond == True:

                for i in range(delta_days.days + 1):
                    
                    day = first_day + timedelta(i)

                    self.TODAY()

                    if day == self.today - timedelta(days=2)  or day == self.today - timedelta(days=1) or day == self.today:

                        case = True
                    
                    elif delta_days.days >= 6:

                        case = False

                    else:

                        case = False

                    temps = self.Request(day.strftime("%Y-%m-%d"), case)

                    self.Tmin_today = temps[0]
                    self.Tmax_today = temps[1]

                    self.GDD_TODAY_CALCULATOR()
                    self.TOTAL_GDD += self.GDD_TODAY
                    self.today = day

                    DATE = self.today
                    T_MIN_CELSIUS = self.Tmin_today
                    T_MAX_CELSIUS = self.Tmax_today
                    GDD_TODAY = self.GDD_TODAY
                    GDD_ACUMULATED = self.TOTAL_GDD

                    D = Dates(Date=DATE, Pest= self.pest, Nearest_location= self.location, T_min_celsius=T_MIN_CELSIUS,  T_max_celsius=T_MAX_CELSIUS, GDD_Today=GDD_TODAY, GDD_Acumulated=GDD_ACUMULATED)

                    D.save()

                    time.sleep(0.7)

    def GDD_TODAY_CALCULATOR(self):

        avg_temp = (self.Tmin_today + self.Tmax_today)/2

        if avg_temp <= self.Tbase:

            self.GDD_TODAY = 0
        
        else:

            self.GDD_TODAY = avg_temp - self.Tbase

    def GDD_acumulated_today(self):

        self.TODAY()

        day = self.today.strftime("%Y-%m-%d")

        yesterday = (self.today - timedelta(days=1)).date()

        temps = self.Request(day, True)

        self.Tmin_today = temps[0]
        self.Tmax_today = temps[1]

        self.GDD_TODAY_CALCULATOR()

        yesterday_GDDAC = Dates.objects.filter(Nearest_location=self.location, Pest= self.pest, Date= yesterday)
        print(yesterday_GDDAC)
        self.TOTAL_GDD = yesterday_GDDAC[0].GDD_Acumulated + self.GDD_TODAY

        self.TODAY()

        DATE = self.today
        T_MIN_CELSIUS = self.Tmin_today
        T_MAX_CELSIUS = self.Tmax_today
        GDD_TODAY = self.GDD_TODAY
        GDD_ACUMULATED = self.TOTAL_GDD

        D = Dates(Date=DATE, Pest= self.pest, Nearest_location= self.location, T_min_celsius=T_MIN_CELSIUS,  T_max_celsius=T_MAX_CELSIUS, GDD_Today=GDD_TODAY, GDD_Acumulated=GDD_ACUMULATED)

        D.save()

        time.sleep(0.7)

    def get_warning(self):

        warning = ""

        for i in self.warnings:

            for j in self.warnings[i]["range"]:

                if j == round(self.TOTAL_GDD):
                    
                    warning = self.warnings[i]["warning"]

                    break
                else:

                    pass
            
            if warning != "":

                break

        return warning

    def get_data(self):
        
        self.TODAY()

        return {
            "Date": self.today,
            "Warning": self.get_warning()
        }
