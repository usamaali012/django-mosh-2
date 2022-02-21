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
	- We need a way to convert our product (or anyother) object to JSON object.
	- DjangoRestFramework have a class called JSONRenderer which has a method called render(dict) which takes a dictiornaty object and returns a JSON object.
	- But how to convert our model to a dictionary? This is where serializers come into play 
	- Serializer: An object that knows how to convert a model instance (like a product) object to a python dictionary.
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


# Serializing Objects:
	- Now to convert Product model to JSON object we will use both classes, Product and ProductSerializer.
	- This is done by the following code:

	- product = Product.objects.get(pk=id)                    ---> Querying to our database
    - serializer = ProductSerializer(product)                 ---> passing our query to serializer class
    - return Response(serializer.data)                        ---> returning data of serializer object

    - The moment we create this serializer (pass our product to serializer class), this serializer will convert out product to a dictionary.
    - that dictionary is in serializer.data
    - In this implementation we did NOT use render method (to convert dict to JSON) anywhere because all that is done under the hood (in the background).
    - Django itself create render object and pass this dictionary and convert it to JSON.

    - In the response, decimal field becomes as a string field (a default setting in RestFrameWork). To override this:
    - Go to settings.py and define a new settings:
    - REST_FRAMEWORK = {
    -	'COERCE_DECIMAL_TO_STRING': False
	-	}

	- To raise an exception, if the product does NOT exist: use try-except block
	- except Product.DoesNotExist:
    -    return Response(status=404)

    - We should avoid using numbers like 404, 500 etc. instead we should use constants as they make our code more readable (a good coding habit)
    - from rest_framework import status  ----> return Response(status=status.HTTP_404_NOT_FOUND)
    - Now this all is a long process. Another short method is to use shortcuts.

    - from django.shortcuts import render, get_object_or_404             
    - get_object_or_404 method will run query itself and if not found gives 404 error
    - This function wraps our try-except block logic.


# Custom Serializer Fields:
	- Objects that we return from our API does NOT necessarily need to look like the Model class that we have in our application.
	- Reason is Data Models are really implementation details of our application.
	- The implementations may change in the future. May add new fileds, or modify existing fields etc.
	- But wo do NOT want these changes to be exposed to the outside world. (remote example)
	- Our API represents Interface of our application, so we should try to make it as stable as possible, otherwise existing clients may break.
	- If you want to change an API, you have to properly study the impact of change and potentially provide different versions of our API.
	- We can also add fields to show in our API that do NOT exist in our model class.

	- serializers.SerializerMethodField(method_name='calculate_tax')
	- SerializerMethodField: a field which is calculated by a method, it takes up a method name which will return the value for this field.
	- Type-Annotation ====>>>> product: Product

	- We can rename our fields for the APIs, it does NOT have to be the same as defined in the model.
	- All we have to do for the field that we have renamed is give a source from where this value is coming from, from the Model class.
	- And every serializer object has an attribute source:
	- price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')


# Serializing Relationships:
	- Few ways to add a related models in our API response. 
	
	- 1) Primary Key 
	- Add a field in serilaized class using PrimaryKeyRelatedField which will take a queryset object as an argument in the related class:
	- collection = serializers.PrimaryKeyRelatedField(queryset=Collection.objects.all())
	- so with this we can include primary-key od the id of each collection in a product object.

	- 2) String: Return the name of each collection
	- collection = serializers.StringRelatedField()
	- This will give us the string representation of the collection class.
	- But for that we first need to load the collection field in our query, otherwise it will run a separate query for collection for each product.
	- queryset = Product.objects.select_related('collection').all()

	- 3) Nested Object: By including a nested object in product object.
	- For that we need to create a separate CollectionSerializer class.
	- And in ProductSerialier class add this line:
	- collection = CollectionSerializer()

	- 4) Hyperlink: Instead of including nested object, we can inckude a hyperlink to an endpoint for viewing that collection.
	- The collection in ProductSerializer class will include a field with HyperlinkedRelatedField which will take two arguments. A queryset object in related class and view_name.
	- view_name argument is used for generating hyperlinks:
	- collection = serializers.HyperlinkedRelatedField(queryset=Collection.objects.all(),view_name='collection-detail')
	- we also need to create a view for this view_name in views file. And add an endpoint for this in urls file.
	- The name you used in view_name, use it in urls file while creating an endpoint for this:
	- path('collections/<int:pk>/', views.collection_detail, name='collection-detail')    
	- remember to use pk and not id in above line and also in collection_detail(request, pk) view. 
	- also add 'context={'request': request}' while initializing ProductSerializer object.
	- serializer = ProductSerializer(queryset, many=True, context={'request': request})


# Model Serializers:
	- Uptill now we have to create models in two places. First Model classes, and then Serializer classes.
	- On a big scale, this can become a huge problem while modifying models.
	- There must be a better way:
	- For this we use Model Serializers:
	- Using the Model Serializers class we can quickly create a Serializers without all the duplications. 
	- Create a Model Serializers class:
	
	- class ProductSerializer(serializers.ModelSerializer):
    -     class Meta:
    -         model = Product
    -         fields = ('id', 'title', 'price', 'collection')               ---> Order Matters

    - Django rest_framework will read the mentioned fields from the mentioned model and create serialize fields itself.
    - for related class (collection), this approach returns the primary key of that related class.
    - you can override this by creating a HyperlinkedRelatedField like we did previously.
    - similarly you can add fields here and can create it in this class to overrider the fields from model class. 

    - To include all these fields, you can simply write:
    - fields = __all__
    - Try to avoid this as much as you can as this is a bad practice. (Not every field should be exposed to outside world)
    - Separate external and internal representations.


# Deserializing:
	- Opposite of Serializing (Happens when we receive data from clients)
	- User wants to create a Product, For that:
	- We shoud send a POST request to /products endpoint, In the body of request we should a include product object.
	- Now on the server, we need to read the data in the body of the request and Deserialize it so we get product object and store in database.
	- To make a request POST or anyother type other than GET, First we need to pass an array as an argument in @api_view() Decorator of that request
	- We have to pass an array of string which specifies the HTTP methods that we support at this endpoint.
	- We did NOT do it earlier as GET is supported by default.
	- Now the serializer we created for the serializing the data can also deserialize, we just have to pass the body of request to the data argument of our serializer class.
	- Now the desrialize data will be in validated_data attribute, but before we access this we should validate our data.


# Data Validation:
	- Before we can access the validated data attribute, first we have to validate the data
	- You must call `.is_valid()` before accessing `.validated_data`
	- 400 ---> Bad Request
	
	- if serializer.is_valid():
    -        return Response('ok')
    -    else:
    -        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    - To avoid this if-else block:
    - serializer.is_valid(raise_exception=True)

    - Django returns an OrderedDict if data we are sending in request is valid.
    - OrderedDict([('title', 'hello'), ('unit_price', Decimal('1.00')), ('collection', <Collection: collection1>)])
    - As part of deserializing the data, djangoRestFramework automatically retrieves a collection with the id we specified. And now we have a collection object here too.

    - Validation at the Object Level:
    - There are situation where validating the request data involves comparing multiple fields. (User Registration --> Password and Confirm Password)
    - For that, we need to override validate method in our 'serializer' class:

    - def validate(self, data):
	-    if data['password'] != data['confirm_password']:
    -        return serializers.ValidationError('Password and Confirm Password must match')
    - return data


# Saving Data/Objects:
	- ProductSerializer class is inheriting from ModelSerializer class.
	- ModelSerializer has a save method that we can use for creating/updating a product.

	- serializer.save()

	- while using "save()" we do not need to call "serializer.validated_data" because it happens in the background hen we use "save()" method.
	
	- To override how a product (object) is created. Either want to include a special field or assosiate a product with another object in the database.
	- For that, we need to override create method in our 'serializer' class:
	- create() is also one of the methods that exist in the base ModelSerializer class. called by the save() method if we try to create a new product

	- def create(self, validated_data):
    -    product = Product.objects.create(**validated_data)
    -    product.other = 1
    -    product.save()
    -    return product 
 
    - Similarly, we have update() method for updating the product (object)

    - def update(self, instance, validated_data):                         # instance = product object
    -    instance.unit_price = validated_data.get('unit_price') 
    -    instance.save()
    -    return instance

    - But in this case, we do NOT need to use update() method. We can rely on djangoRestFrameWork to automatically set all these fields for us.
    - save() method will call one of create() or update() method depending on state of the serializers.

    - For updating a product we need to update product_detail method (because a only product with a certain id can be updated, not all) and we have to use either PUT or PATCH request 
    - 'PUT': For updating all properties
    - "PATCH": For updating few properties
    - Sometimes we only want to update subset of properties (Not All). In that case we will only support 'PATCH' method
    - @api_view(['GET', 'PUT'])

    - elif request.method == 'PUT':
	-   product = get_object_or_404(Product, pk=id)
    -    serializer = ProductSerializer(product, data=request.data)
    -    serializer.is_valid(raise_exception=True)
    -    serializer.save()
    -    return Response(serializer.data)

    - we are passing two things to 'ProductSerializer', request.data and product instance.
    - request.data is for deserialization to happen
    - if we pass product instance, the 'ProductSerializer' will try to update the attributes of that product using the data in the (data=request.data)
    - When i will call the save() method here, it will call the update method, because we are instantiating with an existing product and some data to be serialized.
    - After creating or updating an object, the RestFul convention is to return the object created/updated in the response.
    - When your endpoint creates a new resource, it should return a response with a status code of 201.

{
	"title": "a",
	"slug": "a",
	"unit_price": 1,
	"inventory": 1,
	"collection": 1
}

# Deleting Data/Objects:
	- This will also go in "product_detail" view function. Because this is where we work with the particular product,
	- @api_view(['GET', 'PUT', 'DELETE'])
	- This will bring up a DELETE button in our Browsable api interface.
	- Implementing this function: (Another condition)

	- elif request.method == 'DELETE':
    -   product.delete()
    -   return Response({'error': 'Product cannot be deleted because it is associated with an order item'} ,status=status.HTTP_405_METHOD_NOT_ALLOWED)

    - Another RestFul Convention is, when we delete a response we return an empty response with status code of 204. Its a convention not a rule.
    - Delete method can raise an exception due to foriegnkey constraint.
    - So, for that do some error handling.

    - elif request.method == 'DELETE':
        if collection.products.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it includes one or more products'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    - elif request.method == 'DELETE':
        if product.orderitems.count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item'} ,status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)