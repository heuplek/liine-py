import datetime, bisect
from fastapi import FastAPI
import dataParse

sorted_dict = dataParse.parseData("restaurants.csv")

#class to allow for easy access to the close_hour field of the sorted_dict for binary search
class DictList(object):
    def __init__(self, data, key):
        self.data = data
        self.key = key
    def __getitem__(self, i):
        return self.data[i][self.key]
    def __len__(self):
        return self.data.__len__()

data_close_times = DictList(sorted_dict, "close_ts")
data_start_times = DictList(sorted_dict, "open_ts")


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the restaurant API!"}


@app.get("/restaurants/{date}")
async def find_restaurants(date: datetime.datetime = None):
    #add 1 for the day of the week because the datetime module starts at 0 for monday
    day = date.weekday() + 1 
    time = date.time()
    #convert input to DHHMM string(int)
    str_time = str(day) + time.strftime("%H%M")
    open_restaurants = binary_search(sorted_dict, day, str_time)
    if(len(open_restaurants) == 0):
        return {"open_restaurants": "No restaurants are open at this time."}
    #break down date time into day of week and time.
    return {"open_restaurants": open_restaurants}

def binary_search(data, day, time_stamp):
    #returns the start and end index of the data that contains the time_stamp 
    #(inclusive of open and close hours so Mon at 10PM will include restaurants that close at 10PM on Monday)
    i = bisect.bisect_left(data_close_times, int(time_stamp))
    r = bisect.bisect_right(data_start_times, int(time_stamp))
    open_restaurants = []
    open_restaurants = [x['restaurant'] for x in data[i:r]]

    return open_restaurants

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)