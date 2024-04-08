import os, sys, csv, re, datetime

'''================================================================================================
Function to parse human readable restaurant data into a dictionary of restaurant objects

================================================================================================'''
def parseData(csv_file_name):
    with open((csv_file_name), 'r') as file:
        reader = csv.reader(file)
        # skip the header row
        next(reader)
        return_obj = []
        for row in reader:
            # separate the data into the different fields
            restaurant = row[0]
            hours = row[1]
            hour_rows = mapHours(hours)
            for hour_row in hour_rows:
                hour_row["restaurant"] = restaurant
            if len(hour_rows) == 0:
                print("No hours found for", restaurant)
            return_obj.extend(hour_rows)
        sorted_list = sorted(return_obj, key=lambda k: k['open_ts'])
        return sorted_list
            
                
'''================================================================================================
Take the human readable hours and convert them into a 5 digit int for the day and a 4 digit int for the time
================================================================================================'''

def mapHours(hours):
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    rows = []
    parts = hours.split(" / ")
    pattern = r'((?:[a-zA-Z]{3},\s)?[a-zA-Z]{3}-[a-zA-Z]{3}(?:,\s[a-zA-Z]{3})?|[a-zA-Z]{3})\s([\d]{1,2}(?::[\d]{2})?\s[ap]m\s-\s[\d]{1,2}(?::[\d]{2})?\s[ap]m)'
    matches = re.findall(pattern, hours)
    if not matches:
        print("csv data not in expected formats")
    for match in matches:
        #deal with 'ues'
        if 'ues' in match[0]:
            match = (match[0].replace("ues", "Tue"), match[1])
        #Day ranges:
        if '-' in match[0] and ',' not in match[0]:
            rows.extend(handle_day_range(match, days))
        #Single day
        elif len(match[0]) == 3:
            rows.extend(handle_single_day(match, days))
        #Single day with a range
        elif '-' in match[0] and ',' in match[0]:
            split_days = match[0].split(", ")
            for index, range_or_day in enumerate(split_days):
                if '-' in range_or_day:
                    new_match = (split_days[index], match[1])
                    rows.extend(handle_day_range(new_match, days))
                else:
                    new_match = (split_days[index], match[1])
                    rows.extend(handle_single_day(new_match, days))
        else:
            print("New case found", match)
    return rows

'''================================================================================================
Normalize the hours to a int(string)
================================================================================================'''
def normalize_hours(hour):
    if ":" in hour:
        hours, minutes = hour.split(":")
        if len(hours) == 1:
            hours = "0" + hours
        return hours + minutes
    else:
        if len(hour) == 1:
            hour = "0" + hour
        return hour + "00"

'''================================================================================================
Convert the time to 24 hour time
================================================================================================'''
def to24(hour):
    time, period = hour.split(" ")
    if period == "PM".casefold():
        time = normalize_hours(time)
        #Noon
        if int(time) == int(1200):
            return ("1200")
        else:
            time_plus_twelve = int(time) + 1200
            return (str(time_plus_twelve))
    else:
        time = normalize_hours(time)
        if int(1200) <= int(time) <= int(1299):
            #Midnight
            if(int(time) == 1200):
                return ("0000")
            #midnight to 1 am
            else:
                return "00" + str(int(time) - 1200)
        return (str(time))

'''================================================================================================
Handles csv hour data that includes a '-' in the day field
================================================================================================'''
def handle_day_range(match, days):
    start, end = match[0].split("-")
    if len(start) > 3:
        start = start[:3]
    if len(end) > 3:
        end = end[:3]

    #days
    start = days.index(start) + 1 
    end = days.index(end) + 1
    #hours
    open_hour, close_hour = match[1].split(" - ")
    open_hour = to24(open_hour)
    close_hour = to24(close_hour)
    
    #first handle the cases where the restaurant closes after midnight
    rangeRows = []   
    for i in range(start, end+1):
        if(int(close_hour) < int(open_hour)):
            rangeRows.extend(handle_close_after_midnight(close_hour, open_hour, i))
            rangeRows.append({"open_ts": convert_time_stamp_string(i, open_hour), "close_ts": convert_time_stamp_string(i, "2400")})
        else:
            rangeRows.append({"open_ts": convert_time_stamp_string(i, open_hour), "close_ts": convert_time_stamp_string(i, close_hour)})
    return rangeRows

'''================================================================================================
Handles csv hour data that includes a single day
================================================================================================'''      
def handle_single_day(match, days):
    rows = []
    day = days.index(match[0]) + 1
    open_hour, close_hour = match[1].split(" - ")
    open_hour = to24(open_hour)
    close_hour = to24(close_hour)
    if(int(close_hour) < int(open_hour)):
        rows.extend(handle_close_after_midnight(close_hour, open_hour, day))
        close_hour = "2400"
    rows.append({"open_ts": convert_time_stamp_string(day, open_hour), "close_ts": convert_time_stamp_string(day, close_hour)})
    return rows

'''================================================================================================
Handles data that runs over into the next day appends hours for the following day
================================================================================================'''
def handle_close_after_midnight(close_hour, open_hour, day):
    row_return = []
    if close_hour == ("0000"):
        row_return.append({"open_ts": convert_time_stamp_string(day, open_hour), "close_ts": convert_time_stamp_string(day, "2400")})
    else:
        if(day == 7):
            day = 1
        else:
            day = day+1
        row_return.append({"open_ts": convert_time_stamp_string(day, "0000"), "close_ts": convert_time_stamp_string(day, close_hour)})
    return row_return

'''================================================================================================
simple function to convert day and time to a single int
================================================================================================'''
def convert_time_stamp_string(day, time):
    str_combined = str(day)+str(time)
    return int(str_combined)

if __name__ == "__main__":
    print("Parsing data")
    parseData()