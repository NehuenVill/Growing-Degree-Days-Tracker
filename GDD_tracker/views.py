from django.shortcuts import render, redirect
from django.http import HttpResponse
from GDD_tracker.models import *
from GDD_tracker.GDD_calculator import *
from datetime import datetime

# Create your views here.
#{{DATES_and_GDDS|get_GDD:forloop.counter0}}
#{{DATES_and_GDDS|get_GDD:forloop.counter0}}
#from GDD_tracker.models import Tracker
#objs = Tracker.objects.all()
#objs.delete()

def index(Request):

    form = TrackerForm()

    context = {"form": form}

    if Request.method == 'POST':

        context = {"form": form}

        form = TrackerForm(Request.POST)
        if form.is_valid():
            form.save()

        return redirect("/")

    else:

        form = TrackerForm()
        context = {"form": form}

        return render(Request, "index.html", context)

def trackers(Request):

    trck = Tracker.objects.all()

    dates_and_GDDs = []

    TRCK = []
    
    counter = 0

    for i in trck:

        try:

            if i.Date.date() != datetime.now().date():

                if i.Date != None:
                    GDD_obj = GDD(i.Pest, i.Date, i.Nearest_location)

                    print("first")

                    result = GDD_obj.get_data()
                    
                    i.warning = result["Warning"]

                    i.Date = result["Date"]
                    
                    i.save()

                else:
                    print("second")
                    GDD_obj = GDD(i.Pest, i.Start_date, i.Nearest_location)

                    result = GDD_obj.get_data()
                    
                    i.warning = result["Warning"]

                    i.Date = result["Date"]
                    
                    i.save()


                dates = Dates.objects.filter(Pest= i.Pest, Nearest_location= i.Nearest_location)

                print(dates)

                days = []
                gddac = []
                
                for j in dates:

                    days.append(j.Date.strftime("%m-%d-%y"))
                    gddac.append(j.GDD_Acumulated)

                dates_and_GDDs.append({
                    "DATES" : days,
                    "GDDAC": gddac
                })

                counter += 1

            else:
                print("third")
                print(i.Date.date())
                print(datetime.now().date())

                dates = Dates.objects.filter(Pest= i.Pest, Nearest_location= i.Nearest_location)

                print(dates)
                
                days = []
                gddac = []

                for j in dates:

                    days.append(j.Date.strftime("%m-%d-%y"))
                    gddac.append(j.GDD_Acumulated)

                dates_and_GDDs.append({
                    "DATES" : days,
                    "GDDAC": gddac
                })

                counter += 1

        except:

            if i.Date != None:
                print("fourth")
                GDD_obj = GDD(i.Pest, i.Date, i.Nearest_location)

                result = GDD_obj.get_data()
                    
                i.warning = result["Warning"]

                i.Date = result["Date"]
                    
                i.save()

            else:
                print("fifth")
                GDD_obj = GDD(i.Pest, i.Start_date, i.Nearest_location)

                result = GDD_obj.get_data()
                    
                i.warning = result["Warning"]

                i.Date = result["Date"]
                    
                i.save()


            dates = Dates.objects.filter(Pest= i.Pest, Nearest_location= i.Nearest_location)

            print(dates)
            days = []
            gddac = []
                
            for j in dates:

                days.append(j.Date.strftime("%m-%d-%y"))
                gddac.append(j.GDD_Acumulated)

            dates_and_GDDs.append({
                    "DATES" : days,
                    "GDDAC": gddac
                })

            counter += 1

        TRCK.append({
            "Start_date": i.Start_date,
            "Nearest_loc": i.Nearest_location,
            "Pest": i.Pest,
            "Warning": i.warning,
        })

    TRCK.reverse()

    print(dates_and_GDDs)

    dates_and_GDDs.reverse()

    context = {"trackers": TRCK, "DATES_and_GDDS": dates_and_GDDs}

    return render(Request, "tracker_page.html", context) 