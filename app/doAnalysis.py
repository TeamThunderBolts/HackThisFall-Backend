from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
# import speech_recognition as sr
# import librosa
import json,spacy
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

def isSubstring(s1, s2):
    if s1 in s2:
        return s2.index(s1)
    return -1

def doAnalysis(RecordingSID,templateID):
    # path = "https://api.twilio.com/2010-04-01/Accounts/AC0e147db91380cd72ba1fd1addaa41512/Recordings/RE6b49416e6ae2ffafa8394e1b46462d93"
    s=""
    fillers = ["Well","um","uh","Hmm","Like","Actually","Basically","Seriously", "Right","mhm","uh","huh","You see","You know","I mean","You know what I mean","At the end of the day","Believe me",
                        "I guess","I suppose","Or something","Okay so"]
    spacy.load('en_core_web_sm')
    spacy_stopwords = spacy.lang.en.stop_words.STOP_WORDS

    fillersInS = []

    for word in spacy_stopwords:
        k = isSubstring(word.lower(),s.lower())
        if(k!=-1):
            fillersInS.append(word)
    
    jsonRes = json.dumps([fillersInS])
    jsonRes = json.loads(jsonRes)

    return Response(jsonRes)