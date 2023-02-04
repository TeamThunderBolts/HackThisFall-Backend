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

@api_view(['GET'])
def doAnalysis(request):
    # path = "https://api.twilio.com/2010-04-01/Accounts/AC0e147db91380cd72ba1fd1addaa41512/Recordings/RE6b49416e6ae2ffafa8394e1b46462d93"
    fillerWordList = ["Well","um","uh","Hmm","Like","Actually","Basically","Seriously", "Right","mhm","uh","huh"]
    fillerPhraseList =  ["You see","You know","I mean","You know what I mean","At the end of the day","Believe me",
                        "I guess","I suppose","Or something","Okay so"]
    # r = sr.Recognizer()
    spacy.load('en_core_web_sm')
    spacy_stopwords = spacy.lang.en.stop_words.STOP_WORDS
    # with sr.AudioFile(path) as source:
        # try:
        #     s = (r.recognize_google(r.listen(source)))
        # except:
        #     print("Some unknown error occured! Try again. ")
        # timeDuration = librosa.get_duration(filename=path)
    s = "Hi, I am ashutosh aswani. I am from Vadodara, Gujrat. You Know, I am fourth year student at IIIT Vadodara."
    # wpm = (len(s.split(" "))*60)/timeDuration/
    fillerWordsInS = []
    fillerPhrasesInS = []

    for word in spacy_stopwords:
        k = isSubstring(word.lower(),s.lower())
        if(k!=-1):
            fillerWordsInS.append(word)

    for word in fillerPhraseList:
        k = isSubstring(word.lower(),s.lower())
        if(k!=-1):
            fillerPhrasesInS.append(word)
    
    jsonRes = json.dumps([fillerWordsInS,fillerPhrasesInS])
    jsonRes = json.loads(jsonRes)

    return Response(jsonRes)