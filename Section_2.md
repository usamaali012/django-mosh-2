# RESTFul APIs: (Application Programming Interface)
	- We need a way to expose our data to our client.
	- This is where APIs come.
	- Building an API is building an interface which a client can use to get or save data.
# REST:
	- Representational State Transfer
	- REST defines a bunch of rules for client and server to communicate. Gives us many benefits.
	- There are a lot of rules for this.
	- But practically we need to know about 3.
	- i) Resources
	- ii) Resource Representation
	- iii) HTTP Methods


# 1. RESOURCES:
	- A resource in an API is like an object in our application. e.g., Product, Collection, Cart etc.
	- These resources are available on the web and client applications can access them using a URL.
# URL:
	- Uniform Resource Locator.
	- Its a way to locate a resource on the web.
	- Basically a web address.
	- somthing.com/products
	- somthing.com/products/1            ---> Individual
	- Nested Resource
	- somthing.com/products/1/reviews    ---> reviews of a certain product
	-somthing.com/products/1/reviews/1   ---> One review of a certain product

	- You should NOT nest your resources too deep.
	- Two levels are fine.


# 1. RESOURCES REPRESENTATION:
	- We can identify a resource using its URL.
	- When we hit that URL the server is going to return that resource in a certain format or representation.HTML, XML, JSON etc.
	- None of these are internal representation of a resource on the server.
	- On the server we identify a resource (like a Product) using an object or an instance of a Python class. 
	- But when we return that object to the client, we will represent it as HTML, XML, or JSON format.
	- Because these are the formats client understand.
	- We can use one or multiple representations.
	- If we support multiple representations, client should tell the server what representations it needs when asking for data.
# JSON:
	- JavaScript Object Notation.
	- Its a notation we use for representing objects in Javascript.
	- Key-Value Pair.
	- Keys are always string ----> Should always be sorrounded by double-quotes.
	- Values can be of any data type.


# HTTP Methods:
	- When building a RESTful API, we expose one or more endpoints for clients.
	- Each endpoint may support various kind of operations.
	- Some allow only reading data some might allow modifying data too.
	- This is where HTTP Methods come into play.
	- Using HTTP method the client can tell the server what it wants to do with the resource.
	
	- GET: For getting a resource or a collection of resources.
	- POST: For creating a resource
	- PUT: For updating a resource
	- PATCH: For updating part of a resource. Subset of properties
	- DELETE: For deleting a resource

	- We want to create a product.
	- Send a POST request to /products endpoint
	- POST /products
	- We will also insert a JSON object in the body of the request.
	- Similar for other request too.


# VIEWS:
	- view function: we create a function that takes a request and returns an instance of Httpresponse class in django.
	- In Django we have two classes--> HttpRequest, HttpResponse
	- But DjangoRestFramework also comes with its own Request and Response classes.
	- These classes are more simpler and more powerful than the ones that comes with Django.
	- For using Request class of DjangoRestFramework ----> from rest_framework.decorators import api_view
	- Now if you apply above decorator to your view functon, the request object that the function receives will become an instance of Request class that comes with DjangoRestFramework.
	- So, this will replace the request object in Django witht the newer request object that comes with the DjangoRestFramework which is simpler,
	- For response -->from rest_framework.response import Response.
	- @api_view()
	- def product_list(request):
    - 	return Response('ok')
    - Now with these few simple changes, if you refresh your page, we get a beautiful page which is called Browsable API.
    - This Browsable API makes it incredibly easy to test our API endpoints in the browser.
    - Note That:  You only see this page if you hit your endpoint in a browser.
    - If a client app like a mobile app hit this endpoint, its not going to see the browsable API.
    - Its only going to see the data in the response.
    - To see what client app is going to see, click on the dropdown menu attaches with GET and click on JSON, you will only see the data in the response.

    - Browsable API Page:
    - Page Header:  ---> Generated on the basis of our view function.
    - Next we have information about our request. Request Type and endpoint (GET /store/products/)
    - And then we can see the information about the response: 
    - Status of response:   (HTTP 200 OK)
    - Allow: Tells us what HTTP methods are supported by this endpoint. (Allow: GET, OPTIONS)
    - OPTIONS: To see what operations or what methods are availabe.
    - GET: The method we are using in the request.
    - Content-Type: Tell us the type of the content in the response.    (Content-Type: application/json)
    - Vary:  ???
    - And then we have body of the response.


# Serializer:
	- We need a way to convert our product (or anyother) object ti JSON object.
	- DjangoRestFramework have a class called JSONRenderer which has a method called render(dict) which takes a dictiornaty object and returns a JSON object.
	- But how to convert our model to a dictionary ? This is where serializers come into play 
	- Serializer: An object that knows how to convert a model instance (like a product object to a python dictionary)
	- create a new file serializers.py and import ---> from rest_framework import serializers
	- Now make a class that inherits from serializers.Serializer. -->  class ProductSerializer(serializers. Serializer):
	- Now in this class we have to decide which fileds of the Product class we want to include to be in python dictionary
	- We can have a lots of fields in our model class but what we return from the API does NOT necessarily have to have all the fields from the model class. 
	- Because what we have in our model class is internal representation of our class (Product) 
	- And what we return from our API is the external representation of the Product.
	- You might have sensitive information in the class which you cannot expose to outside world.
	- That is why you have two types of representations.
	- Now here we have to define our fields exactly like we defined our fields in the model class.
	- Pretty much everything that we need to create a model in our Model Class is available in serializers class like all the fields such as BooleanField, IntegerField, StringField etc. 
	- And all thes fields have a bunch of core arguments that are available everywhere, like read_only, Write_only, required (which is ser to True by default), default and so on.
	- But certain fields depending on their type are also support additional arguments.
	- So this is exactly like we define our model. 
	- We will also use these serializer when receiving data from out API.
	- We do NOT have to name our fields exactly like they are defined in model class.
	- Because this is a completely separate class from the Product Model that we defined earlier. Name of the field do NOT even have to match.
	- But for consistency define it as it is in the Model class.
	
	- class ProductSerializer(serializers. Serializer):
    - 	id = serializers.IntegerField()
    - 	title = serializers.CharField(max_length=255)
    - 	unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)

    - Now that we have a serializer, we can use it to convert a Product object to a Python dictionary.


 