from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from .models import *
from .apps import *
import requests
import re
import json


@api_view(['POST'])
def taskCreate(request):
    data_request = request.data
    input_model = request.data["message_babel"]
    print("POST ON LEO-BABEL  --> {}".format(input_model))

    jsonarray_r = requests.post('http://127.0.0.1:8881/', json={"sentence": "{}".format(str(input_model))})
    jsonarray = jsonarray_r.json()

    list_auth_lang = ["fr", "en"]
    if (float(jsonarray['score'])) > 0.8 and (jsonarray['language'] in list_auth_lang) and (len(input_model.split())) > 4:
        serializer = TaskSerializer(data={'message_babel': '{}'.format(
            input_model), 'langue_babel': '{}'.format(jsonarray['language'])})
        if serializer.is_valid():
            serializer.save()
        return JsonResponse(jsonarray, safe=False)
    else:
        serializer = TaskSerializer(data={'message_babel': '{}'.format(
            input_model), 'langue_babel': 'NC'})
        if serializer.is_valid():
            serializer.save()
        return JsonResponse(jsonarray, safe=False)


@api_view(['GET'])
def taskList(request):
    tasks = Task.objects.all().order_by('-id')
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def taskList_orange(request):
    tasks_orange = OrangeDB.objects.all().order_by('-id')
    serializer_orange = TaskSerializer_orange(tasks_orange, many=True)
    return Response(serializer_orange.data)


@api_view(['GET'])
def taskList_red(request):
    tasks_red = RedDB.objects.all().order_by('-id')
    serializer_red = TaskSerializer_red(tasks_red, many=True)
    return Response(serializer_red.data)


@api_view(['GET'])
def taskList_yellow(request):
    tasks_yellow = YellowDB.objects.all().order_by('-id')
    serializer_yellow = TaskSerializer_yellow(tasks_yellow, many=True)
    return Response(serializer_yellow.data)


@api_view(['GET'])
def taskList_pink(request):
    tasks_pink = PinkDB.objects.all().order_by('-id')
    serializer_pink = TaskSerializer_pink(tasks_pink, many=True)
    return Response(serializer_pink.data)


@api_view(['GET'])
def taskList_blue(request):
    tasks_blue = BlueDB.objects.all().order_by('-id')
    serializer_blue = TaskSerializer_blue(tasks_blue, many=True)
    return Response(serializer_blue.data)


@api_view(['GET'])
def taskList_green(request):
    tasks_green = GreenDB.objects.all().order_by('-id')
    serializer_green = TaskSerializer_green(tasks_green, many=True)
    return Response(serializer_green.data)


@api_view(['DELETE'])
def taskDelete(request, pk):
    tasks = Task.objects.get(id=pk)
    tasks.delete()
    return Response('Item Deleted')


@api_view(['DELETE'])
def taskDeleteOrange(request, pk):
    tasksDorange = OrangeDB.objects.get(id=pk)
    tasksDorange.delete()
    return Response('Item Deleted')


@api_view(['DELETE'])
def taskDeleteRed(request, pk):
    tasksDred = RedDB.objects.get(id=pk)
    tasksDred.delete()
    return Response('Item Deleted')


@api_view(['DELETE'])
def taskDeleteYellow(request, pk):
    tasksDyellow = YellowDB.objects.get(id=pk)
    tasksDyellow.delete()
    return Response('Item Deleted')


@api_view(['DELETE'])
def taskDeletePink(request, pk):
    tasksDpink = PinkDB.objects.get(id=pk)
    tasksDpink.delete()
    return Response('Item Deleted')


@api_view(['DELETE'])
def taskDeleteBlue(request, pk):
    tasksDblue = BlueDB.objects.get(id=pk)
    tasksDblue.delete()
    return Response('Item Deleted')


@api_view(['DELETE'])
def taskDeleteGreen(request, pk):
    tasksDgreen = GreenDB.objects.get(id=pk)
    tasksDgreen.delete()
    return Response('Item Deleted')