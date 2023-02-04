from urllib import response
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view
import json, os, environ
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
    tagret_name = body['target_name']
    target_phone = body['target_phone']
    target = {
        "company_username" : company_username,
        "target_name" : target_phone,
        "target_phone":target_phone
    }
    query_object = queries.PyMongo()
    result = query_object.add('targets',target)
    return JsonResponse("Success", safe=False)

@api_view(['POST'])
def templates_list(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    username = body['username']
    query_object = queries.PyMongo()
    result = query_object.get('templates','username',str(username))
    return HttpResponse(result)

@api_view(['POST'])
def targets_list(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    company_username = body['company_username']
    query_object = queries.PyMongo()
    result = query_object.get('targets','company_username',str(company_username))
    return HttpResponse(result)

@api_view(['POST'])
def create_campaign(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    company_username = body['company_username']
    targets = body['targets']
    templates_id = body['template_id']
    campaign = {
        "company_username" : company_username,
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
    for target in targets:
        query_object = queries.PyMongo()
        result = query_object.get('targets','_id',ObjectId(target))
        result = (json.loads(dumps(list(result))))[0]['target_phone']
        path = os.getcwd() + "app\.env"
        env=environ.Env(
            DEBUG=(bool,False)
        )
        environ.Env.read_env(path)

        auth_id = env('AUTH_ID')
        auth_token = env('AUTH_TOKEN')
        endpoint = env('HTTP_PY_ENDPOINT')

        client = Client(auth_id,auth_token)

        call = client.calls.create(
                                url=endpoint+'get_xml/'+str(template_id),
                                to=str(result),
                                from_='+13855267353'
                            )
    return HttpResponse("Success")
    
@api_view(['POST'])
def twilio_xml(request,template_id):
    query_object = queries.PyMongo()
    result = query_object.get('templates','_id',ObjectId(template_id))
    result = dumps(list(result))
    result = json.loads(result)
    result=result[0]
    response_obj = VoiceResponse()
    response_obj.say(result['usecases']['1']['Question'])
    path = os.getcwd() + "app\.env"
    env=environ.Env(
        DEBUG=(bool,False)
    )
    environ.Env.read_env(path)
    endpoint = env('HTTP_PY_ENDPOINT')
    response_obj.record(timeout=10,transcribe=True,finishOnKey='#',transcribe_callback=endpoint+'handler/1/'+str(template_id),method='POST')
    return HttpResponse(response_obj)

@api_view(['POST'])
def twilio_handler(request,index,template_id):
    next_index = int(index)
    answer = "answer from abhay will come here"
    response_obj = VoiceResponse()
    response_obj.say(answer)

    query_object = queries.PyMongo()
    result = query_object.get('templates','_id',ObjectId(template_id))
    result = dumps(list(result))
    result = json.loads(result)
    result=result[0]
    if str(next_index) in result['usecases']:
        response_obj.say(result['usecases'][str(next_index)]['Question'])
    path = os.getcwd() + "app\.env"
    env=environ.Env(
        DEBUG=(bool,False)
    )
    environ.Env.read_env(path)
    endpoint = env('HTTP_PY_ENDPOINT')
    response_obj.record(timeout=10,transcribe=True,finishOnKey='#',transcribe_callback=endpoint+'handler/'+str(next_index)+'/'+str(template_id),method='POST')

    return HttpResponse(response_obj)
