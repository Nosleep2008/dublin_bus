import joblib
import pandas as pd
import requests
from datetime import datetime

def getOneCall(UnixTime):
    url = 'https://api.openweathermap.org/data/2.5/onecall?lat=53.3477767&lon=-6.2676788&appid=dbb2b9eb4f9424b9c2c168ad52c077d9'
    response = requests.get(url)
    data = response.json()
    result = {}
    Hour0Time = int(data['hourly'][0]['dt'])
    Hour48Time = int(data['hourly'][47]['dt'])
    print(UnixTime,Hour0Time,Hour48Time)
    if int(UnixTime) < Hour0Time:
        return result
    elif int(UnixTime) > Hour48Time:
        print(data['daily'][7]['dt'])
        if int(UnixTime) > int(data['daily'][7]['dt']):
            return result
        day = (int(UnixTime) - int(Hour0Time)) / (3600 * 24) + 2
        temp = data['daily'][int(day)]['temp']['day']
        feels_like = data['daily'][int(day)]['feels_like']['day']
        wind_speed = data['daily'][int(day)]['wind_speed']
        wind_deg = data['daily'][int(day)]['wind_deg']
        clouds_all = data['daily'][int(day)]['clouds']
        weather_main = data['daily'][int(day)]['weather'][0]['main']
    else:
        hour = (int(UnixTime) - int(Hour0Time)) / 3600
        temp = data['hourly'][int(hour)]['temp']
        feels_like = data['hourly'][int(hour)]['feels_like']
        wind_speed = data['hourly'][int(hour)]['wind_speed']
        wind_deg = data['hourly'][int(hour)]['wind_deg']
        clouds_all = data['hourly'][int(hour)]['clouds']
        weather_main = data['hourly'][int(hour)]['weather'][0]['main']
    result['temp'] = temp
    result['feels_like'] = feels_like
    result['wind_speed'] = wind_speed
    result['wind_deg'] = wind_deg
    result['clouds_all'] = clouds_all
    result['weather_main'] = weather_main
    return result


def prediction(routeName, passengerArrivalTime, stopId):
    """routeName is string
    passengerArrivalTime is date object
    stopId is string"""
    route = 'model_files/' + str(routeName) + '.pkl'
    time = pd.to_datetime(passengerArrivalTime)
    df = pd.read_csv('model_files/one_row.csv')
    save = ['temp', 'feels_like', 'wind_speed', 'wind_deg', 'clouds_all', 'Hour']
    df[save] = df[save].astype('object')
    uint8 = df.select_dtypes(include=['int64']).columns
    df[uint8] = df[uint8].astype('uint8')
    df[['temp', 'feels_like', 'wind_speed', 'Hour']] = df[['temp', 'feels_like', 'wind_speed', 'Hour']].astype(
        'float64')
    df[['wind_deg', 'clouds_all']] = df[['wind_deg', 'clouds_all']].astype('int64')
    #######################
    unixTime = datetime.timestamp(time)
    #print(datetime.fromtimestamp(unixTime))
    time = pd.Series(time)
    hour = (time.dt.minute/60)[0] + time.dt.hour[0]
    month = time.dt.month[0]
    day = time.dt.day[0]
    week = time.dt.dayofweek[0]
    stop = stopId
    ############
    data = getOneCall(unixTime)
    if data == {}:
        return "input date invalid!"
    model = joblib.load(route)

    df[['weather_main_' + data['weather_main']]] = 1
    df[['Day_' + str(day)]] = 1
    df[['week_' + str(week)]] = 1
    df[['Month_' + str(month)]] = 1
    df['Hour'] = hour
    df['temp'] = data['temp']
    df['feels_like'] = data['feels_like']
    df['wind_speed'] = data['feels_like']
    df['wind_deg'] = data['wind_deg']
    df['clouds_all'] = data['clouds_all']
    #print(df)
    ###############
    arrival_time = model.predict(df)
    unixTime = unixTime + float(arrival_time[0])
    print(float(arrival_time[0]))
    readableTime = datetime.fromtimestamp(unixTime)
    return str(readableTime)[0:19]


a = prediction('1', '2020-07-23 21:54:10', '2323')
print(a)

