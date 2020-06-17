import requests
import datetime
import time


def timeStampConvert(timeString):
    """Convert the datetime in string into timestamp"""
    timestamp = time.mktime(datetime.datetime.strptime(timeString, "%d/%m/%Y %H:%M:%S").timetuple())
    return int(timestamp)


def getRTPI(stopid):
    """Get Real-Time Passenger Information(RTPI) for dublin transportation,
    taking in the stop ID,and a list of dicts will be returned.
    Wrong stop ID will lead to a None return."""

    url = "https://data.smartdublin.ie/cgi-bin/rtpi/realtimebusinformation?stopid=" + str(stopid) + "&format=json"

    RTPI_json = requests.get(url).json()

    errorCode = int(RTPI_json['errorcode'])
    result = RTPI_json['results']

    # if input a wrong stop ID, function will return None
    if errorCode:
        return None

    # Return the result of specific stop ID, with route, arrival time,
    # schedule time, due time, destination, origin, current timestamp
    real_time_info = []
    for i, routeInfo in enumerate(result):
        real_time_dict = {}

        route = routeInfo["route"]
        # By the way convert the datetime into timestamp type
        real_time_dict[route] = {"dueTime": routeInfo["duetime"],
                                 "origin": routeInfo["origin"],
                                 "destination": routeInfo["destination"],
                                 "currentTime": int(time.time()),
                                 "arrivalTime": timeStampConvert(routeInfo["arrivaldatetime"]),
                                 "scheduleTime": timeStampConvert(routeInfo["scheduledarrivaldatetime"]),
                                 }

        real_time_info.append(real_time_dict)

    return real_time_info
