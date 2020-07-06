from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def route(request):
    # Result display the request as a demo
    result = [{'status': 'test'}]
    # Return the response as a dictionary to AJAX
    return JsonResponse(result, safe=False)