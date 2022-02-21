from re import L
from webbrowser import get
from django.db.models.aggregates import Count
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
# from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import ListCreateAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Collection, Product
from .serializers import CollectionSerializer, ProductSerializer
from store import serializers

# Create your views here.
# def product_list(request):
#     return HttpResponse('ok')


class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer

    # def get_queryset(self):
    #     return Product.objects.select_related('collection').all()

    # def get_serializer_class(self):
    #     return ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}



# class ProductList(APIView):
#     def get(self, request):
#         queryset = Product.objects.select_related('collection').all()
#         serializer = ProductSerializer(queryset, many=True, context={'request': request})  # many=True --> for serilizer to know it should iterate over the queryset and convert each product object to dictionary 
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)                     # raise_exception=True --> if serializer is not valid, it will raise an exception
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)



# @api_view(['GET', 'POST'])
# def product_list(request):
#     if request.method == 'GET':
#         queryset = Product.objects.select_related('collection').all()
#         serializer = ProductSerializer(queryset, many=True, context={'request': request})  # many=True --> for serilizer to know it should iterate over the queryset and convert each product object to dictionary 
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)                     # Either this line,or if-else block below is required to raise exception if serializer is not valid
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
        
#         # if serializer.is_valid():
#         #     return Response('ok')
#         # else:
#         #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ProductDetail(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        if product.orderitems.count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item'} ,status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)                



# @api_view(['GET', 'PUT', 'DELETE'])
# def product_details(request, id):
#     product = get_object_or_404(Product, pk=id)
#     if request.method == 'GET':
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         if product.orderitems.count() > 0:
#             return Response({'error': 'Product cannot be deleted because it is associated with an order item'} ,status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

#     # try:
#     #     product = Product.objects.get(pk=id)
#     #     serializer = ProductSerializer(product)
#     #     return Response(serializer.data)
#     # except Product.DoesNotExist:
#     #     # return Response(status=404)
#     #     return Response(status=status.HTTP_404_NOT_FOUND)



class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer

    def get_serializer_context(self):
        return {'request': self.request}



# class CollectionList(APIView):
#     def get(self, request):
#         queryset = Collection.objects.annotate(products_count=Count('products')).all()
#         serializer = CollectionSerializer(queryset, many=True, context={'request': request}) 
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = CollectionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)              
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)



# @api_view(['GET', 'POST'])
# def collection_list(request):
#     if request.method == 'GET':
#         queryset = Collection.objects.annotate(products_count=Count('products')).all()
#         serializer = CollectionSerializer(queryset, many=True, context={'request': request}) 
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = CollectionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)              
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)



@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request, pk):
    collection = get_object_or_404(
        Collection.objects.annotate(products_count=Count('products')), 
        pk=pk)
    if request.method == 'GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if collection.products.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it includes one or more products'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)