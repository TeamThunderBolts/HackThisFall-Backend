from urllib import response
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view
import json
from pymongo import MongoClient
import environ

# Create your views here.
env=environ.Env(
    DEBUG=(bool,False)
)
environ.Env.read_env("\.env")

connection_string = env('connection_string')
client = MongoClient(connection_string)
db = client['callbot']
collection_name = db["users"]

@api_view(['POST'])
def signup(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    username = body['username']
    password = body.get('password')
    company_name = body.get('company_name')
    result = username
    user = {
        "username" : username,
        "password" : password,
        "company_name" : company_name
    }
    collection_name.insert_many([user])
    return JsonResponse("Success", safe=False)
