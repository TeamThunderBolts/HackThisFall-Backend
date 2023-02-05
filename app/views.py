from urllib import response
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view
import json, os, environ
from twilio.twiml.voice_response import VoiceResponse, Say
from app import queries
from app.doAnalysis import doAnalysis
from bson.json_util import dumps
from twilio.rest import Client
from bson.objectid import ObjectId
from bson.json_util import dumps

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
    target_name = body['target_name']
    target_phone = body['target_phone']
    target = {
        "company_username" : company_username,
        "target_name" : target_name,
        "target_phone":target_phone
    }
    query_object = queries.PyMongo()
    result = query_object.add('targets',target)
    return JsonResponse("Success", safe=False)

@api_view(['POST'])
def templates_list(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    company_username = body['company_username']
    query_object = queries.PyMongo()
    result = query_object.get('templates','username',str(company_username))
    result = list(result)
    json_result = dumps(result, indent = 2)
    return JsonResponse(json.loads(json_result), safe = False)

@api_view(['POST'])
def targets_list(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    company_username = body['company_username']
    query_object = queries.PyMongo()
    result = query_object.get('targets','company_username',str(company_username))
    result = list(result)
    json_result = dumps(result, indent = 2)
    return JsonResponse(json.loads(json_result), safe = False)

@api_view(['POST'])
def create_campaign(request):
    print(1)
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
    print(2)
    query_object = queries.PyMongo()
    result = query_object.add('campaigns',campaign)
    print(3)
    send_campaign(campaign)
    print(4)
    return JsonResponse("Success", safe=False)

def send_campaign(body):
    username = body['company_username']
    targets = body['targets']
    template_id = body['template_id']
    print(5)
    for target in targets:
        print(6)
        query_object = queries.PyMongo()
        result = query_object.get('targets','_id',ObjectId(target))
        result = (json.loads(dumps(list(result))))[0]['target_phone']
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        environ.Env.read_env(env_file=os.path.join(BASE_DIR, '.env'))

        auth_id = os.getenv('AUTH_ID')
        auth_token = os.getenv('AUTH_TOKEN')
        endpoint = os.getenv('HTTP_PY_ENDPOINT')

        client = Client(auth_id,auth_token)

        print(endpoint)
        call = client.calls.create(
                                url=endpoint+'get_xml/'+str(template_id),
                                to=str(result),
                                from_='+13855267353')
    
@api_view(['POST'])
def twilio_xml(request,template_id):
    print(8)
    query_object = queries.PyMongo()
    result = query_object.get('templates','_id',ObjectId(template_id))
    result = dumps(list(result))
    result = json.loads(result)
    result=result[0]
    response_obj = VoiceResponse()
    response_obj.say(result['usecases']['1']['Question'])
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    environ.Env.read_env(env_file=os.path.join(BASE_DIR, '.env'))
    print(9)
    endpoint = os.getenv('HTTP_PY_ENDPOINT')
    response_obj.record(timeout=10,transcribe=True,finishOnKey='#',transcribe_callback=endpoint+'handler/1/'+str(template_id),method='POST')
    print(10)
    return HttpResponse(response_obj)

@api_view(['POST'])
def twilio_handler(request,index,template_id):
    next_index = int(index)+1
    RecordingSID = (json.loads(request.body))['RecordingSID']
    print(RecordingSID)
    # answer = doAnalysis(RecordingSID,template_id,next_index)
    if(next_index!=4):
        answer="answer from abhay"
    else:
        answer=""
    response_obj = VoiceResponse()

    # 1
    response_obj.say(answer)

    if answer=="":
        return HttpResponse(response_obj)

    query_object = queries.PyMongo()
    result = query_object.get('templates','_id',ObjectId(template_id))
    result = dumps(list(result))
    result = json.loads(result)
    result=result[0]
    print(12)

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    environ.Env.read_env(env_file=os.path.join(BASE_DIR, '.env'))
    endpoint = os.getenv('HTTP_PY_ENDPOINT')
    
    if str(next_index) in result['usecases']:
        print(13)

        # 2
        response_obj.say(result['usecases'][str(next_index)]['Question'])

        # 3
        response_obj.record(timeout=10,transcribe=True,finishOnKey='#',transcribe_callback=endpoint+'handler/'+str(next_index)+'/'+str(template_id),method='POST')

    print(14)
    return HttpResponse(response_obj)
