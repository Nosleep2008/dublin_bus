import json
from datetime import datetime

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from dublin_bus.models import Favourite

from dublin_bus import arrival_prediction


def index(request):
    return render(request, 'index.html')


def planner(request):
    with open("./data_files/routes_stops.json", 'r') as f:
        Dict = json.load(f)
    return render(request, 'contact.html', {
        'routes_stops': json.dumps(Dict)
    })


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
            startStop = step['startStop']
            endStop = step['endStop']
            routeName = step['lineName']
            passengerArrivalTime = lastStepEndTime
            print("what inside google>>>")
            print(step)
            print(startStop,endStop)
            # If stop id does not exist

            #if startStop.get('id') == None or endStop.get('id') == None:
            is_route_exsit = arrival_prediction.check_routes(routeName)
            if is_route_exsit:
                # If stop id does exist
                #startStopId = startStop['id']
                #endStopId = endStop['id']
                passengerArrivalTime_str = str(datetime.fromtimestamp(passengerArrivalTime))
                print(passengerArrivalTime_str)
                passengerWaitingTime = arrival_prediction.prediction(routeName,startStop,endStop,passengerArrivalTime_str)

                if isinstance(passengerWaitingTime, float):
                    transitArrivalTime = passengerWaitingTime + passengerArrivalTime
                else:
                    # Use the depart time estimated by google maps api as transitArrivalTime
                    transitArrivalTime = int(
                        datetime.timestamp(
                            datetime.strptime(
                                step['googleDepart']['value'], '%Y-%m-%dT%H:%M:%S.%fZ'
                            )))
                    passengerWaitingTime = transitArrivalTime - passengerArrivalTime

                print("test")
                print(passengerWaitingTime)
                print(passengerArrivalTime)
            else:
                # Use the depart time estimated by google maps api as transitArrivalTime
                transitArrivalTime = int(
                    datetime.timestamp(
                        datetime.strptime(
                            step['googleDepart']['value'], '%Y-%m-%dT%H:%M:%S.%fZ'
                        )))
                passengerWaitingTime = transitArrivalTime - passengerArrivalTime
            transitArrivalTime_str = datetime.utcfromtimestamp(transitArrivalTime).strftime('%Y-%m-%d %H:%M:%S')

            transitArrivalTime_str = datetime.utcfromtimestamp(transitArrivalTime).strftime('%Y-%m-%d %H:%M:%S')

            stepResultDict = {'travelMode': 'BUS',
                              'routeName': routeName,
                              'transitArrivalTime': transitArrivalTime_str,
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


def login(request):
    if request.method == "GET":
        context = {'previous_page': request.GET.get('from_page')}
        return render(request, 'login.html', context)
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            return HttpResponse('Account name or password is incorrect')
            # return render(request, 'error.html', {'message': 'Account name or password is incorrect.'})


def register(request):
    if request.method == "GET":
        context = {'previous_page': request.GET.get('from_page')}
        return render(request, 'register.html', context)
    else:
        try:
            username = request.POST['username']
            password = request.POST['password']
            # Justify the user exist or not
            if User.objects.filter(username=username).exists():
                context = {'register_info': True, 'previous_page': request.GET.get('from_page')}
                return render(request, 'register.html', context)
            else:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                return HttpResponseRedirect(request.GET.get('from_page'))
        except:
            return HttpResponse('Exception in registration, please try again.')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(request.GET.get('from_page'))

@csrf_exempt
def favourite(request):

    user = request.POST.get('username')
    origin = request.POST.get('start')
    destination = request.POST.get('end')

    f = Favourite(username=user, origin=origin, destination=destination)
    f.save()

    favourite = Favourite.objects.filter(username=user).values_list('origin','destination')
    favourite = list(favourite)
    result = [{'favourite': favourite}]

    return JsonResponse(result, safe=False)


@csrf_exempt
def show_favourite(request):
    user = request.POST.get('username')

    favourite = Favourite.objects.filter(username=user).values_list('origin', 'destination')
    favourite = list(favourite)
    result = [{'favourite': favourite}]

    return JsonResponse(result, safe=False)

@csrf_exempt
def delete_favourite(request):

    user = request.POST.get('username')
    origin = request.POST.get('start')
    destination = request.POST.get('end')

    f = Favourite.objects.get(username=user, origin=origin, destination=destination)
    f.delete()

    favourite = Favourite.objects.filter(username=user).values_list('origin','destination')
    favourite = list(favourite)
    result = [{'favourite': favourite}]

    return JsonResponse(result, safe=False)

@csrf_exempt
def team15_prediction(request):
    errorcode = 0;
    routeName = request.POST.get('route')
    start_stop = request.POST.get('start')
    end_stop = request.POST.get('end')
    depart_time = request.POST.get('depart_time')
    #print(depart_time)
    duration = arrival_prediction.prediction(routeName,start_stop, end_stop, depart_time)

    result = [{'errorcode': errorcode, 'duration': duration[0], 'start_time':duration[1]}]
    return JsonResponse(result, safe=False)
