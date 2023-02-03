from urllib import response
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view
import json
from app import queries

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
    query_object = queries.PyMongo()
    query_object.add('users',user)
    return JsonResponse("Success", safe=False)
