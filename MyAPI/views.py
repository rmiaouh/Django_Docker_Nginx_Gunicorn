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
    print("OK1")
    jsonarray_r = requests.post('http://rmiaouh.site:8081/', json={"sentence": "{}".format(str(input_model))})
    #jsonarray_r = None
    jsonarray = jsonarray_r.json()
    print("OK2")
    print(jsonarray)
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


@api_view(['POST'])
def taskCreate_orange(request):
    data_request = request.data
    input_model = request.data["message_orange"]
    print("POST ON LEO-ORANGE  --> {}".format(input_model))
    try:
        r = requests.post('http://rmiaouh.site:8082/',
                          json={'sentence': str(input_model)})
        prev_sentence = str(input_model)
        print(r.json())
        for i in range((len(r.json()['data']))):
            print('ok1')
            dcolor = "#ec611b"
            dtext = (output_data_date['data'][i]['text'])
            print('ok2')
            ddim = (output_data_date['data'][i]['dim'])
            print('ok3')
            dvalue = (output_data_date['data'][i]['value']['value'])
            print('ok4')
            replace_by = """<mark class="entity" style="background: {dcolor}; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em">
                    <b title="{dvalue}
                    ">{dtext}</b>
                    <span style="font-size: 0.8em; font-weight: bold; line-height: 3; border-radius: 0.35em; text-transform: uppercase; vertical-align: middle; margin-left: 0.5rem" title="Free Web tutorials">{ddim}</span>
                </mark>""".format(dcolor=dcolor, dtext=dtext, ddim=ddim, dvalue=dvalue)
            prev_sentence = re.sub(
                r'\b' + str(dtext) + r'\b', replace_by, prev_sentence)
        jsonarray = prev_sentence
        print('ok5')
        serializer = TaskSerializer_orange(data={'message_date': '{}'.format(
            input_model), 'dim_date': '{}'.format(ddim), 'text_date': '{}'.format(dtext), 'value_date': '{}'.format(dvalue), 'color_date': '{}'.format(dcolor), 'output_date': '{}'.format(prev_sentence)})
        print('ok6')
        if serializer.is_valid():
            serializer.save()
            print('save1')
        print("return 1")
        return JsonResponse(jsonarray, safe=False)
    except:
        serializer = TaskSerializer_orange(data={'message_date': '{}'.format(
            input_model), 'output_date': '{}'.format(
            input_model)})
        if serializer.is_valid():
            serializer.save()
            print('save2')
        print("return 2")
        return JsonResponse(input_model, safe=False)


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
