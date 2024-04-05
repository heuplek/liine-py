'''================================================================================================
Function to parse human readable restaurant data into a dictionary of restaurant objects to 
store in the database.


================================================================================================'''
import os, sys, csv, re, datetime

def parseData():
    #print("Parsing data")
    #print(os.path.join(sys.path[0], "data\restaurants.csv"))
    if os.path.exists(os.path.join(sys.path[0], "data/restaurants.csv")):
        with open(os.path.join(sys.path[0], "data/restaurants.csv"), 'r') as file:
            reader = csv.reader(file)
            # skip the header row
            next(reader)
            returnObj = []
            for row in reader:
                # separate the data into the different fields
                restaurant = row[0]
                hours = row[1]
                #print(restaurant)
                hourRows = mapHours(hours)
                for hourRow in hourRows:
                    hourRow["restaurant"] = restaurant
                if len(hourRows) == 0:
                    print("No hours found for", restaurant)
                returnObj.extend(hourRows)
                #print(returnObj)
            return returnObj
            
                




def mapHours(hours):
    # postgres DOW is 0-6, Sun-Sat
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    rows = []
    parts = hours.split(" / ")
    pattern = r'((?:[a-zA-Z]{3},\s)?[a-zA-Z]{3}-[a-zA-Z]{3}(?:,\s[a-zA-Z]{3})?|[a-zA-Z]{3})\s([\d]{1,2}(?::[\d]{2})?\s[ap]m\s-\s[\d]{1,2}(?::[\d]{2})?\s[ap]m)'
    matches = re.findall(pattern, hours)
    if not matches:
        print("No matches found")
    for match in matches:
        #print(match)
        #deal with 'ues'
        if 'ues' in match[0]:
            match = (match[0].replace("ues", "Tue"), match[1])
        #days in match[0], hours in match[1]
        #Day ranges:
        if '-' in match[0] and ',' not in match[0]:
            rows.extend(handleDayRange(match, days))
        elif len(match[0]) == 3:
            rows.append(handleSingleDay(match, days))
        elif '-' in match[0] and ',' in match[0]:
            splitDays = match[0].split(", ")
            #print(splitDays)
            for index, rangeOrDay in enumerate(splitDays):
                if '-' in rangeOrDay:
                    newMatch = (splitDays[index], match[1])
                    rows.extend(handleDayRange(newMatch, days))
                else:
                    newMatch = (splitDays[index], match[1])
                    rows.append(handleSingleDay(newMatch, days))
        else:
            print("PROBLEMMMMMM")
    return rows

def normalizeHours(hour):
    #print(hour)
    if ":" in hour:
        hours, minutes = hour.split(":")
        if minutes == "00":
            return float(hours)
        elif minutes == "15":
            return float(hours) + 0.25
        elif minutes == "30":
            return float(hours) + 0.5
        elif minutes == "45":
            return float(hours) + 0.75
    else:
        return hour
    
def to24(hour):
    time, period = hour.split(" ")
    if period == "PM".casefold():
        time = normalizeHours(time)
        #handle noon
        if int(time) == int(12):
            return (str(datetime.timedelta(hours=float(time)))[:-3])
        else:
            time_plus_twelve = float(time) + 12
            return (str(datetime.timedelta(hours=time_plus_twelve))[:-3])
    else:
        time = normalizeHours(time)
        return (str(datetime.timedelta(hours=float(time)))[:-3])

def handleDayRange(match, days):
    start, end = match[0].split("-")
    if len(start) > 3:
        start = start[:3]
    if len(end) > 3:
        end = end[:3]
    #print(start,"through", end)
    start = days.index(start)
    end = days.index(end)
    #start end has the day range in numbers
    #print(start, end)
    openHour, closeHour = match[1].split(" - ")
    openHour = to24(openHour)
    
    #print("opens at", openHour)
    closeHour = to24(closeHour)
    #print("closes at", closeHour)
    rangeRows = []
    for i in range(start, end+1):
        if i == 6:
            day = 0
        else:
            day = i+1
        rangeRows.append({"day": day, "open_hour": openHour, "close_hour": closeHour})
    return rangeRows
        
    #should be able to stash this in a database now

def handleSingleDay(match, days):
    #print(match[0])
    day = days.index(match[0])
    openHour, closeHour = match[1].split(" - ")
    openHour = to24(openHour)
    #print("opens at", openHour)
    closeHour = to24(closeHour)
    #print("closes at", closeHour)
    #normalize day to Sunday-Saturday for postgres
    if day == 6:
        day = 0
    else:
        day = day+1
    return {"day": day, "open_hour": openHour, "close_hour": closeHour}


