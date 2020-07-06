import json
from datetime import datetime

from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, 'index.html')


@csrf_exempt
def route(request):
    # Initialise the response variable
    totalWalkingTime = 0
    totalWalkingDistance = 0
    totalTransitTime = 0
    totalWaitingTime = 0

    # Take the steps list from the request
    routeInfo = request.POST.get('routeInfo')
    routeInfo = json.loads(routeInfo)
    steps = routeInfo['steps']

    # Depart Time
    # Get time in json format
    departTime = routeInfo['departTime']
    # Turn time into datetime object in python
    departTime = datetime.strptime(departTime, '%Y-%m-%dT%H:%M:%S.%fZ')
    # Turn time into timestamp (integer)
    departTime = int(datetime.timestamp(departTime))

    # The time tag that record the end time of every step to calculate the waiting time between two steps
    # For the first step the last step end time is the depart time
    lastStepEndTime = departTime
    stepsResult = []
    print(lastStepEndTime)
    for i, step in enumerate(steps):
        travelMode = step['travelMode']
        stepResultDict = {}
        # Step by walking
        if travelMode == 'WALKING':
            totalWalkingTime += step['googleDuration']['value']
            totalWalkingDistance += step['distance']['value']
            lastStepEndTime += step['googleDuration']['value']
            stepResultDict = {'travelMode': 'WALKING'}

        # Step by tram(LUAS)
        if travelMode == 'TRAM':
            routeName = step['lineName']
            passengerArrivalTime = lastStepEndTime
            # Use the depart time estimated by google maps api as transitArrivalTime
            transitArrivalTime = int(
                datetime.timestamp(
                    datetime.strptime(
                        step['googleDepart']['value'], '%Y-%m-%dT%H:%M:%S.%fZ'
                    )))
            passengerWaitingTime = transitArrivalTime - passengerArrivalTime
            stepResultDict = {'travelMode': 'TRAM',
                              'routeName': routeName,
                              'transitArrivalTime': transitArrivalTime,
                              'estimateWaitingTime': passengerWaitingTime
                              }

            totalWaitingTime += passengerWaitingTime
            totalTransitTime += step['googleDuration']['value']
            # Use the depart time estimated by google maps api
            lastStepEndTime = transitArrivalTime + step['googleDuration']['value']

        # Step by bus
        if travelMode == 'BUS':
            routeName = step['lineName']
            passengerArrivalTime = lastStepEndTime
            # Use the depart time estimated by google maps api as transitArrivalTime
            transitArrivalTime = int(
                datetime.timestamp(
                    datetime.strptime(
                        step['googleDepart']['value'], '%Y-%m-%dT%H:%M:%S.%fZ'
                    )))
            passengerWaitingTime = transitArrivalTime - passengerArrivalTime
            stepResultDict = {'travelMode': 'BUS',
                              'routeName': routeName,
                              'transitArrivalTime': transitArrivalTime,
                              'estimateWaitingTime': passengerWaitingTime
                              }

            totalWaitingTime += passengerWaitingTime
            totalTransitTime += step['googleDuration']['value']
            # Use the depart time estimated by google maps api
            lastStepEndTime = transitArrivalTime + step['googleDuration']['value']

        stepsResult.append(stepResultDict)

    # Result display the request as a demo
    result = [{'walkingTime': totalWalkingTime,
               'walkingDistance': totalWalkingDistance,
               'transitTime': totalTransitTime,
               'totalEstimateWaitingTime': totalWaitingTime,
               'stepsInfo': stepsResult}]
    # Return the response as a dictionary to AJAX
    return JsonResponse(result, safe=False)
