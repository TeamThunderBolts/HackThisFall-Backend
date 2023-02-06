from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
# import speech_recognition as sr
# import librosa
import json,spacy
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from app import queries
from bson.json_util import dumps

def isSubstring(s1, s2):
    if s1 in s2:
        return s2.index(s1)
    return -1

@api_view(['POST'])
def doAnalysis(request):
    # path = "https://api.twilio.com/2010-04-01/Accounts/AC0e147db91380cd72ba1fd1addaa41512/Recordings/RE6b49416e6ae2ffafa8394e1b46462d93"
    s=""
    fillers = ["Well","um","uh","Hmm","Like","Actually","Basically","Seriously", "Right","mhm","uh","huh","You see","You know","I mean","You know what I mean","At the end of the day","Believe me",
                        "I guess","I suppose","Or something","Okay so"]
    spacy.load('en_core_web_sm')
    spacy_stopwords = spacy.lang.en.stop_words.STOP_WORDS

    words = s.lower().split()

    # fillersInS = []

    # for word_stop in spacy_stopwords:
    #     for word in words:
    #         if word == word_stop:
    #             fillersInS.append(word)
        # k = isSubstring(word.lower(),s.lower())
        # if(k!=-1):
        #     fillersInS.append(word)
    
    query_object = queries.PyMongo()
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    company_username = body['company_username']
    query_object = queries.PyMongo()
    result = query_object.get('templates','username',str(company_username))
    result = list(result)

    json_result = dumps(result, indent = 2)
    result = json.loads(json_result)

    count = 0
    for word in words : 
        for tag in result:
            print(tag)
            if tag == word:
                count = count+1
                break

    return JsonResponse({"Count" : result}, safe = False)