from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
# def product_list(request):
#     return HttpResponse('ok')

@api_view()
def product_list(request):
    return Response('ok')

@api_view()
def product_details(request, id):
    return Response(id)