from urllib import response
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view
import json
from twilio.twiml.voice_response import VoiceResponse, Say
from app import queries
from bson.json_util import dumps
from twilio.rest import Client
from bson.objectid import ObjectId

@api_view(['POST'])
def signup(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    username = body['username']
    password = body.get('password')
    company_name = body.get('company_name')
    user = {
        "username" : username,
        "password" : password,
        "company_name" : company_name
    }
    query_object = queries.PyMongo()
    query_object.add('users',user)
    return JsonResponse("Success", safe=False)

@api_view(['POST'])
def login(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    username = body['username']
    password = body.get('password')
    user = {
        "username" : username,
        "password" : password,
    }
    query_object = queries.PyMongo()
    result = query_object.find('users',user)
    if result:
        return JsonResponse("Valid", safe=False)
    else : 
        return JsonResponse("Invalid", safe=False)

@api_view(['POST'])
def add_target(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    company_username = body['company_username']
    tagret_name = body['tagret_name']
    target_phone = body['target_phone']
    target = {
        "company_username" : company_username,
        "tagret_name" : target_phone,
        "target_phone":target_phone
    }
    query_object = queries.PyMongo()
    result = query_object.add('targets',target)
    return JsonResponse("Success", safe=False)

@api_view(['POST'])
def templates_list(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    username = body['company_username']
    query_object = queries.PyMongo()
    result = query_object.get('templates','username',str(username))
    return HttpResponse(result)

@api_view(['POST'])
def targets_list(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    username = body['company_username']
    query_object = queries.PyMongo()
    result = query_object.get('targets','company_username',str(username))
    return HttpResponse(result)

@api_view(['POST'])
def create_campaign(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    username = body['company_username']
    targets = body['targets']
    templates_id = body['template_id']
    campaign = {
        "company_username" : username,
        "targets" : targets,
        "template_id":templates_id
    }
    query_object = queries.PyMongo()
    result = query_object.add('campaigns',campaign)
    send_campaign(campaign)
    return JsonResponse("Success", safe=False)

def send_campaign(body):
    username = body['company_username']
    targets = body['targets']
    template_id = body['template_id']
    xml_object = twilio_xml(template_id)
    print(xml_object)
    for target in targets:
        print("--->",target)
        query_object = queries.PyMongo()
        result = query_object.get('targets','_id',ObjectId(target))
        result = (json.loads(dumps(list(result))))[0]['target_phone']
        print(result)
        client = Client("AC0e147db91380cd72ba1fd1addaa41512", "805f5e15ad0395a5d35fcf4856436e76")

        call = client.calls.create(
                                url='https://callbot-fxb6-onrender.com/get_xml/'+str(template_id),
                                to=str(result),
                                from_='+13855267353'
                            )
    pass
    
@api_view(['GET'])
def twilio_xml(request,template_id):
    query_object = queries.PyMongo()
    result = query_object.get('templates','_id',ObjectId(template_id))
    result = dumps(list(result))
    result = json.loads(result)
    result=result[0]
    response_obj = VoiceResponse()
    response_obj.say(result['usecases']['1']['Question'])
    response_obj.record(timeout=10, transcribe=True)
    response_obj.say("end end end")
    return HttpResponse(response_obj)

def twilio_handler(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    campaign_id = body['campaign_id']
    query_object = queries.PyMongo()
    result = query_object.get('campaigns','template')
