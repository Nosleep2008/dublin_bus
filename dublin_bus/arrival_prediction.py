import joblib
import pandas as pd
import requests
from datetime import datetime


def check_routes(id):
    id = str(id)
    df = pd.read_csv('./model_files/routeID.csv')
    arr = df.values.tolist()
    n = []
    for i in arr:
        n.append(i[0])
    #print(n)
    if id in n:
        return True
    else:
        return False


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


def prediction(routeName,stop_start,stop_final,passengerDepartureTime):
    """routeName is string
    passengerArrivalTime is date object
    stopId is string"""
    print("测试传入最原始参数", passengerDepartureTime)
    num = int(passengerDepartureTime[6])
    num = str(num + 1)
    a = passengerDepartureTime[0:6]
    b = passengerDepartureTime[7:]
    passengerDepartureTime = a + num + b

    print("测试传入参数",passengerDepartureTime)
    #print(routeName,stop_start,stop_final,passengerDepartureTime)
    stop_start = int(stop_start)
    stop_final = int(stop_final)
    path = './data_files/' + str(routeName) + '.csv'
    df = pd.read_csv(path)
    time = pd.to_datetime(passengerDepartureTime)
    time = pd.Series(time)
    hour = (time.dt.minute/60)[0] + time.dt.hour[0]
    #month = time.dt.month[0]
    #day = time.dt.day[0]
    week = time.dt.dayofweek[0]

    #  start to get schedule time of final bus stop
    start_hour = hour
    #print(start_hour)
    temp1 = df[df['STOPPOINTID'] == stop_start][df['Hour'] >= start_hour][df['Hour'] <= (start_hour+2)][df['week'] == week]

    if temp1.empty:
        temp1 = df[df['STOPPOINTID'] == stop_start][df['Hour'] >= (start_hour-0.1)]
        temp2 = df[df['STOPPOINTID'] == stop_final]
    else:
        temp2 = df[df['STOPPOINTID'] == stop_final][df['week'] == week]
    #print(temp1)
    #print(temp2)
    re = pd.merge(temp1, temp2, how='inner', on=['TRIPID', 'VEHICLEID'])
    #print(re)
    if re.empty:
        print("no stops pair")
        result = ["no stops pair", " error...."]
        return result
    re = re.sort_values(by=['Hour_x'])
    star_stop_time = re.iat[0, 3]
    final_stop_time = re.iat[0, 7]
    # end to get
    min = (star_stop_time - int(star_stop_time)) * 60
    min = int(round(min))
    '''
    array = passengerDepartureTime.split(" ")
    date1 = array[0].split("-")
    date1[0] = int(date1[0])
    date1[1] = int(date1[1])
    date1[2] = int(date1[2])
    print(date1)

    if date1[1] < 10 and len(date1[1]<=1):
        date1[1] = "0" + date1[1]

    if date1[2] < 10 and len(date1[1]<=1):
        date1[2] = "0" + date1[2]

    date2 = array[1].split(":")
    print(date2)
    if date2[0] < 10 and len(date2[0] <= 1):
        date2[0] = "0" + date2[0]

    if date2[1] < 10 and len(date2[1] <= 1):
        date2[1] = "0" + date2[1]

    if date2[2] < 10 and len(date2[2] <= 1):
        date2[2] = "0" + date2[2]
    date2[0] = int(date2[0])
    date2[1] = int(date2[1])
    date2[2] = int(date2[2])
    passengerDepartureTime = str(date1[0])+"-"+str(date1[1])+"-"+str(date1[2]) + " " +str(date2[0])+":"+str(date2[1])+":"+str(date2[2])
        '''
    if int(star_stop_time) < 10:
        start = "0" + str(int(star_stop_time))
    else:
        start = str(int(star_stop_time))
    passengerDepartureTime = passengerDepartureTime[0:11] + start + ":" + str(min) + ":" + "00"
    print(star_stop_time,final_stop_time,passengerDepartureTime)
    duration = model(routeName, passengerDepartureTime, final_stop_time)
    print("duration",duration)
    if not isinstance(duration,str):
        duration = round(abs(duration), 2)
    result = [duration, " "]
    result[1] = start + ":" + " " + str(min)
    print(result)
    return result


def model(routeName, passengerDepartureTime, passengerArrivalHour):
    """routeName is string
    passengerArrivalTime is date object
    stopId is string"""

    route = './model_files/' + str(routeName) + '.pkl'
    print("passsssssssdtime",passengerDepartureTime)
    time = pd.to_datetime(passengerDepartureTime)
    #print(time)
    df = pd.read_csv('./model_files/one_row.csv')
    save = ['temp', 'feels_like', 'wind_speed', 'wind_deg', 'clouds_all', 'Hour']
    df[save] = df[save].astype('object')
    uint8 = df.select_dtypes(include=['int64']).columns
    df[uint8] = df[uint8].astype('uint8')
    df[['temp', 'feels_like', 'wind_speed', 'Hour']] = df[['temp', 'feels_like', 'wind_speed', 'Hour']].astype(
        'float64')
    df[['wind_deg', 'clouds_all']] = df[['wind_deg', 'clouds_all']].astype('int64')
    #######################
    unixTime = int(datetime.timestamp(time))
    print('i need unix time')
    print(unixTime)
    #print(datetime.fromtimestamp(unixTime))
    time = pd.Series(time)
    hour = (time.dt.minute/60)[0] + time.dt.hour[0]
    month = time.dt.month[0]
    day = time.dt.day[0]
    week = time.dt.dayofweek[0]
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
    depart_time_diff = model.predict(df)
    depart_time = hour
    depart_time_diff = int(depart_time_diff[0])
    ###############
    df["Hour"] = passengerArrivalHour
    arrive_time_diff = model.predict(df)
    arrive_time = passengerArrivalHour
    arrive_time_diff = int(arrive_time_diff[0])
    ################
    duration = arrive_time - depart_time - (depart_time_diff - arrive_time_diff)/3600
    return duration


#if __name__ == '__main__':
#    aaa = prediction("7D",4830,4962,"2020-08-15 5:10:00")
#    print(aaa)
