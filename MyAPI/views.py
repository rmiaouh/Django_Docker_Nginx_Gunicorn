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
import unicodedata


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')


def remove_stopwords_str_lieux(str_data):
    temp = open("./static/assets/blacklist.txt", 'r').readlines()
    # split sentence in list
    wordsFiltered = []
    str_data = str(str_data)
    str_data_list = str_data.split()
    # check if words in list are in the banwords

    for w in str_data_list:

        if w not in temp:
            wordsFiltered.append(w)
    # merge the list in str format
    wordsFiltered = (" ").join(wordsFiltered)
    return wordsFiltered

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
            dtext = (r.json()['data'][i]['text'])
            print('ok2')
            ddim = (r.json()['data'][i]['dim'])
            print('ok3')
            dvalue = (r.json()['data'][i]['value']['value'])
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


@api_view(['POST'])
def taskCreate_yellow(request):
    data_request = request.data
    input_model = request.data["message_yellow"]
    print("POST ON LEO-YELLOW  --> {}".format(input_model))

    try:
        r = requests.post('http://rmiaouh.site:8083/',
                          json={'sentence': str(input_model)})
        # display suggestion term, edit distance, and term frequency
        prev_sentence = str(input_model)
        output_data_ortho = r.json()['data']
        dcolor = "#C9991E"
        dtext = str(output_data_ortho)
        ddim = input_model
        dvalue = "Phrase corrigée"
        replace_by = """<mark class="entity" style="background: {dcolor}; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em">
            <b title="{dvalue}
            ">{dtext}</b>
            <span style="font-size: 0.8em; font-weight: bold; line-height: 3; border-radius: 0.35em; text-transform: uppercase; vertical-align: middle; margin-left: 0.5rem" title="Phrase initiale">{ddim}</span>
            </mark>""".format(dcolor=dcolor, dtext=dtext, ddim=ddim, dvalue=dvalue)
        prev_sentence = re.sub(r'\b' + str(ddim) + r'\b',
                               replace_by, prev_sentence)
        jsonarray = prev_sentence
        print("T3")
        serializer = TaskSerializer_yellow(data={'message_ortho': '{}'.format(
            output_data_ortho), 'output_ortho': '{}'.format(
            prev_sentence)})
        if serializer.is_valid() and (str(input_model).strip() != str(output_data_ortho.strip())):
            print("valid")
            serializer.save()
            return JsonResponse(jsonarray, safe=False)

        else:
            print("else valid")
            serializer = TaskSerializer_yellow(data={'message_ortho': '{}'.format(
            output_data_ortho), 'output_ortho': '{}'.format(
            input_model)})
            if serializer.is_valid():
                serializer.save()
            return JsonResponse(input_model, safe=False)

    except Exception as e:
        print(str(e))
        print("fail ortho")
        serializer = TaskSerializer_yellow(data={'message_ortho': '{}'.format(
            input_model), 'output_ortho': '{}'.format(
            input_model)})
        if serializer.is_valid():
            serializer.save()
        return JsonResponse(input_model, safe=False)

@api_view(['POST'])
def taskCreate_pink(request):
    data_request = request.data
    input_model = request.data["message_pink"]
    print("POST ON LEO-PINK  --> {}".format(input_model))

    try:
        r = requests.post('http://rmiaouh.site:8084/',
                          json={'sentence': str(input_model), 'language': "fr", 'bot_id': "115"})
        output_data_feel = r.json()['data']
        prev_sentence = str(input_model)
        tendance = "NC"
        dcolor = "rgb(170, 70, 132)"
        dtext = str(input_model)
        print(float(output_data_feel['compound']))
        if float(output_data_feel['compound']) <= 0.15 and float(output_data_feel['compound']) >= -0.15:
            tendance = "NEUTRE"
        elif float(output_data_feel['compound']) > 0.20:
            tendance = "POSITIVE"
        elif float(output_data_feel['compound']) < -0.20:
            tendance = "NEGATIVE"
        print(tendance)
        ddim = tendance
        dvalue = "{}".format(output_data_feel)
        prev_sentence = """<mark class="entity" style="background: {dcolor}; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em; color: white">
            <b title="{dvalue}
            ">{dtext}</b>
            <span style="font-size: 0.8em; font-weight: bold; line-height: 3; border-radius: 0.35em; text-transform: uppercase; vertical-align: middle; margin-left: 0.5rem;" title="Tendance">{ddim}</span>
            </mark>""".format(dcolor=dcolor, dtext=dtext, ddim=ddim, dvalue=dvalue)
        jsonarray = prev_sentence
        print("T3")
        serializer = TaskSerializer_pink(data={'message_feel': '{}'.format(
            input_model), 'output_feel': '{}'.format(
            prev_sentence)})
        if serializer.is_valid():
            print("valid")
            serializer.save()
            return JsonResponse(jsonarray, safe=False)
    except Exception as e:
        print(str(e))
        serializer = TaskSerializer_pink(data={'message_feel': '{}'.format(
            output_data_feel), 'output_feel': '{}'.format(
            prev_sentence)})
        if serializer.is_valid():
            print(" not valid")
            serializer.save()
    return JsonResponse(input_model, safe=False)

@api_view(['POST'])
def taskCreate_green(request):
    data_request = request.data
    input_model = request.data["message_green"]
    input_model = remove_stopwords_str_lieux(input_model)
    # here we remove accents
    input_model = strip_accents(input_model.lower())
    print("POST ON LEO-GREEN  --> {}".format(input_model))

    try:
        r = requests.post('http://rmiaouh.site:8085/',
                          json={'sentence': str(input_model), 'language': "fr", 'bot_id': "115"})      
        #output_data_lieux = r.json()['data']
        prev_sentence = str(input_model)
        data_to_dic = json.loads(r.json())
        for datas_lieux in data_to_dic :
            dcolor = "#065f2d"
            for count, items in enumerate(data_to_dic[datas_lieux]):
                dtext = (data_to_dic[datas_lieux][count]["value"])
                print(dtext)
                ddim = datas_lieux
                dvalue = ""
                replace_by = """<mark class="entity" style="background: {dcolor}; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em; color: white">
                        <b title="{dvalue}
                        ">{dtext}</b>
                        <span style="font-size: 0.8em; font-weight: bold; line-height: 3; border-radius: 0.35em; text-transform: uppercase; vertical-align: middle; margin-left: 0.5rem" title="Free Web tutorials">{ddim}</span>
                    </mark>""".format(dcolor=dcolor, dtext=dtext, ddim=ddim, dvalue=dvalue)
                prev_sentence = re.sub(
                    r'\b' + str(dtext) + r'\b', replace_by, prev_sentence)
        jsonarray = prev_sentence
        print("GOGO")
        if len(data_to_dic) == 0:
            serializer = TaskSerializer_green(data={'message_lieux': '{}'.format(
                input_model), 'output_lieux': '{}'.format(input_model)})
        else:
            serializer = TaskSerializer_green(data={'message_lieux': '{}'.format(
                input_model), 'output_lieux': '{}'.format(prev_sentence)})
        if serializer.is_valid():
            serializer.save()
        return JsonResponse(jsonarray, safe=False)
    except Exception as e:
        print(str(e))
        serializer = TaskSerializer_green(data={'message_lieux': '{}'.format(
            input_model), 'output_lieux': '{}'.format(
            input_model)})
        if serializer.is_valid():
            serializer.save()
        return JsonResponse(input_model, safe=False)

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
