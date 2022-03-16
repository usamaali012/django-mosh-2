# Class-based Views:
	- All the views we have created so far, have been function-based views.
	- But djangoRestFramework also supports class-based views, which makes our code more cleaner and concise.
	- and we can reuse the code more often. so, first:

	- from rest_framework.views import APIView

	- APIView class is the base class for all class-based views.

	- Python naming convention for classes ---> ProductListClass  ---> Capital letter for each new word.
	- for functions we are using -----> product_list   -----> all lower case, words seaprated by _ underscore

	- In class we will define two methods, get and post. And the incoming request will automatically dispatch to one of these methods depending on its method.
	- By writing these methods we escape from writing too many if-else conditions
	- change you url file as:
	- path('products/', views.ProductList.as_view())

	- APIView class has a method called as_view(), when we call this method it will convert this class to a regular view function.
	- So at the end, the function is called under the hood.


# Mixins:
	- While defining get and post method in ProductList and CollectionList class we see a lot of similar pattern that is in these methods.
	- We have the almost exact same pattern in both classes with minor differences. 
	- A mixins is a class that encapsulates some pattern of code like this.
	
	- from rest_framework.mixins import ListModelMixin, CreateModelMixin

	- If you look at the ListModelMixin class, we have a list() method which has a logic of listing a bunch of models.
	- It has a similar pattern that we have in our get methods of ProductList, CollectionList.
	- CreateModelMixin class has a create() method which encapsulates the logic for creating a resource.

	- djangoRestFramework guide --> API Views ---> Generic Views ---> On the left you can see all the available mixins.



# Generic Views:
	- Most of the time we are not going to use mixins directly instead we will use Concrete View classes which combines one or more mixins.
	- These Concrete View Classes are called Generic Views.
	- e.g., "ListCreateAPIView" which combines two mixins ListModelMixin and CreateModelMixin.

	- from rest_framework.generics import ListCreateAPIView

	- GenericAPIView is a base class for all generic views.
	- This class provides a bunch of methods which we can override in our custom views. Like get_queryset() to define our queryset and get_serializer_class() to define our serializer.
	- That was the minor difference that we had in our same methods of different APIs.

	- ListCreateAPIView has two methods get() and post() which in turn calls the list() method ListModelMixin and create() method of CreateModelMixin respectively.
	- So, a Generic View is a concrete class that combines one or more mixins and provide handler methods like get, post, put and delete etc.
	
	- djangoRestFramework guide --> API Views ---> Generic Views ---> On the left you can see all the available Concrete View Classes.

	- Inherit from this class "ListCreateAPIView" and override methods get_serializer_class() and get_queryset() and your API is ready.

	- class ProductList(ListCreateAPIView):
	    def get_queryset(self):
	        return Product.objects.select_related('collection').all()
	    def get_serializer_class(self):
	        return ProductSerializer
	    def get_serializer_context(self):
	        return {'request': self.request}

	- Use/Override "serializer_class" and "queryset" attributes if you do NOT have too much logic used in your queryset and serializer class, otherwise use their methods as above.

	- class ProductList(ListCreateAPIView):
    	queryset = Product.objects.select_related('collection').all()
    	serializer_class = ProductSerializer
    	def get_serializer_context(self):
        	return {'request': self.request}

    - Creating class ProductList(ListCreateAPIView), the post method for this asks for products_count as required field which is a actually not a required filed but a filed that we create at the runtime in its serilaizer class. 
    - To make this not required field, we need to set products_count as read_only in serializer class where we defined it.

    - products_count = serializers.IntegerField(read_only=True)


# Custom Generic Views:
	- There are situations where generic views might not work for us. So sometimes we have to customize it.
	- Our "ProductDetailView" provides three operations --->> GET, PUT and DELETE.
	- A generic class for such three operations is "RetrieveUpdateDestroyAPIView"
	- Like above we will pas it two attributes. "queryset" and "serializer_class"
	- And now we do NOT need to write method of "get" and "put" as all of that logic is completely implemented in class "RetrieveUpdateDestroyAPIView"
	which we have inherited.

	- But our "DELETE" method in "ProductDetailView" has a little different logic than in the class "RetrieveUpdateDestroyAPIView". We have some logic that is specific to our application.
	- So here we need to override the "delete" method that we have inherited from "RetrieveUpdateDestroyAPIView" class. 
	- That is how we can customize generic views.

	- While testing this view, we get an error which says:
	- Expected view ProductDetail to be called with a URL keyword argument named "pk". Fix your URL conf, or set the `.lookup_field` attribute on the view correctly.

	- In the url of product detail view, we have given our product id as "id" but out generic view expects it to be "pk". So change it.
	- path('products/<int:pk>/', views.ProductDetail.as_view())

	- Or if you want this to stay as "id", you can set another attribute in your class "lookup_field"
	- lookup_field = "id"

	- If you are setting this to 'pk' then in 'delete' method change 'id' to 'pk'.


# ViewSets:
	- Currently we have two views for managing our products. "ProductList" and "ProductDetail".
	- If paid close attention, we have some duplication acoss these classes. 
	- serializer_class is same in both cases, and queryset is almost same too with a slight difference. We can remove that difference. As do not need to use collection in our Products API.
	- Now our querysets are identical too.
	- Now we have more duplication.
	- And this is we use "ViewSets".
	- Using a "ViewSet", we can combine the logic for multiple related views inside a single class. Its a set of related views.

	- First import ModelViewSet class.
	- from rest_framework.viewsets import ModelViewSet

	- "ModelViewSet" class has multiple has multiple base classes. All the mixins class as well as "GenericViewSet" class.
	- Everything we have learned about "GenericViews" also exist in "GenericViewSet" class.
	- Create a new class "ProductViewSet"  --->> naming convention = Model class name followed by ViewSet.
	- This class should inherit from "ModelViewSet".
	- Because this is also a generic view, here we have "querset" and "serializer_class" attributes and methods too.
	- Now add "queryset" and "serializer_class" attribute and add "get_serializer_context" method.
	- And from "ProductDetail" class, add "delete" method here too.
	- And now you do NOT need both "ProductList" and "ProductDetail" classes.
	- And we are left with "ProductViewSet" class that combines the logic for multiple views.
	- And now we have a single class for implementing the "/products" endpoint.
	- Using this single class, we can list our products, create them, update them and delete them. (A benefit of using ViewSet)

	- But for ViewSet we need to use routers for the urls. (Next Lecture)

	- If we inherit from "ModelViewSet" class we can perform all kind of operations on a resource. e.g., Listing resource, Create resource, Update resource and delete resource.
	- But if you do NOT want to have write operations like creating/updating/deleting etc and just want to be able to read a resource only then you can inherit from another class "ReadOnlyModelViewSet".
	- If we inherit from "ReadOnlyModelViewSet" class, we can only perform read operations. List all objects or a single object. 


# Routers:
	- When we use ViewSets, we are not  going to explicitly register URL patterns, this will be done by router.
	- We will register our ViewSets with a router and the router will take care of generating these URL patterns for us.

	- SIMPLE ROUTER:

	- from rest_framework.routers import SimpleRouter
	- router = SimpleRouter()
	- router.register('products', views.ProductViewSet)              --->> define an endpoint and give it a viewset.
	- router.register('collections', views.CollectionViewSet)

	- Now all the urls are created in "router.url". If you print  router.url you will get the following array.

	- [
		<URLPattern '^products/$' [name='product-list']>,
		<URLPattern '^products/(?P<pk>[^/.]+)/$' [name='product-detail']>,
		<URLPattern '^collections/$' [name='collection-list']>,
		<URLPattern '^collections/(?P<pk>[^/.]+)/$' [name='collection-detail']>
		]

	- Set your urlpatterns equal to this array
	- urlpatterns = router.urls

	- Say you have more URL patterns than those are defined by the "router.urls". Then You can use following code.
	
	- 	urlpatterns = [
    		path('', include(router.urls)),
     		Here define your URL patterns which are not defined by router.urls
     		]

    - DEFAULT ROUTER:
    - Using DefaultRouter, You get two additional features:
    - You get an additional page called ApiRoot @ "http://127.0.0.1:8000/store/"
    - And here you can see various endpoints that are available to us.
    
    - 2nd feature: 
    - If you send request to an API endpoint and append ".json" at the end. You get all your data in JSON format.
    - "http://127.0.0.1:8000/store/products.json" -->> At this endpoint you will get all your products in JSON format,		

    - from rest_framework.routers import DefaultRouter
    - router = DefaultRouter()
	- router.register('products', views.ProductViewSet)              --->> define an endpoint and give it a viewset.
	- router.register('collections', views.CollectionViewSet)

	- Now all the urls are created in "router.url". If you print router.url you will get the following array.


    - [
    	<URLPattern '^products/$' [name='product-list']>,
    	<URLPattern '^products\.(?P<format>[a-z0-9]+)/?$' [name='product-list']>,
    	<URLPattern '^products/(?P<pk>[^/.]+)/$' [name='product-detail']>,
    	<URLPattern '^products/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$' [name='product-detail']>,
    	<URLPattern '^collections/$' [name='collection-list']>,
    	<URLPattern '^collections\.(?P<format>[a-z0-9]+)/?$' [name='collection-list']>,
    	<URLPattern '^collections/(?P<pk>[^/.]+)/$' [name='collection-detail']>,
    	<URLPattern '^collections/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$' [name='collection-detail']>,
    	<URLPattern '^$' [name='api-root']>,
    	<URLPattern '^\.(?P<format>[a-z0-9]+)/?$' [name='api-root']>
    ]

    - PROBLEM:
    - At "http://127.0.0.1:8000/store/products" this endpoint you also see "DELETE" button now which is meant to only show for individual products but not for all of them.
    - In our ViewSets, we should NOT override the "delete" rather we should override "destroy" method.
    - The "delete" method in "RetrieveUpdateDestroyAPIView" also uses "destroy" method.

    - Replace "delete" method of your "ViewSets" with following "destroy" method.


# Building Reviews API:
	- Now we will Introduce Reviews.
	- A given product can have multiple reviews:         ----------->>>>        "http://127.0.0.1:8000/store/products/2/reviews"
	- And we should be able to access individual Reviews like this: -------->>> "http://127.0.0.1:8000/store/products/2/reviews/1"
	- Here we have nested Resources, so we need to talk about nested routers.
	- But before that we need to build our model. "Reviews" Model 

	- 3 Steps for creating a model:
	1) Create a Model Class.
	 	class Review(models.Model):
    		product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    		name = models.CharField(max_length=255)
    		description = models.TextField()
    		date = models.DateField(auto_now_add=True)  
	 		Create a migration
	
	2) Create Migration. 
	- Run the following command in the termial:
	- python manage.py makemigrations

	3) Apply Migration. 
	- Run the following command in the termial:
	- python manage.py migrate

	- 3 steps for buildind an API:
	1) Create a Serializer Class.
		class ReviewSerializer(serializers.ModelSerializer):
    		class Meta:
        		model = Review
        		fields = ['id', 'date', 'name', 'description', 'product']

	2) Create a view
		class ReviewViewSet(ModelViewSet):
    		queryset = Review.objects.all()
    		serializer_class = ReviewSerializer

	3) Register a route  (Either using a router (For ViewSets) or by explicitly registering a URL pattern object)
		- NEXT LECTURE.


# Nested Routers:
	- First, we need to install djangoRestFramework nested-routers.
	
	- pip install drf-nested-routers           (For installing globally)
	- pipenv install drf-nested-routers        (For installing only in venv)

	- Just like we have "SimpleRouter" we also have "NestedSimpleRouter". which we can get from following import.

	- from rest_framework_nested import routers

	- In this module, we have a bunch of router classes.
	- Here we also have "DefaultRouter", "SimpleRouter" just as before and they replaces the classes imported from "rest_framework".
	- They behave the same way as before.
	- We also have "NestedDefaultRouter", "NestedSimpleRouter"
	- "NestedDefaultRouter"
	- We have to pass 3 arguments to this nested function.
	- the parent router, parent prefix, and lookup parameter.
	- Having a lookup means we will have a paremeter in our url with name "lookup_pk" (Here, "lookup" is defined by us.)

	router = routers.DefaultRouter()
	router.register('products', views.ProductViewSet)
	router.register('collections', views.CollectionViewSet 
	products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')          ---------Nested route with 3 paramenters

	- Now we will register this child route as we did for parent routes.
	- Now, in register, we will give 3 arguments.
	- An endpoint, and a mapping class/function to deal with that endpoint (As before)
	- And finally, a 'basename', which is used as a prefix for generating the name of url patterns.

	products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')

	- So, our routes will be, "product-reviews/list" and "product-reviews/detail"
	- Now that we have both parent and child routers, we can combine urls of both these routers and store them in "urlpatterns" object.

	urlpatterns = router.urls + products_router.urls

	- Alternatively, if you set "urlpatterns" to an array, where you have explicit routes, you can use the "include" function to include the urls of these routers.

	- Right now, while creating a review, we explicitly have to assign the product_id.

	{
    	"name": "",
    	"description": "",
    	"product": null
	}

	- But this should NOT be the case, we should get the product_id from our url. We do NOT want to pass the product_id in the request body rather we need to read it from the url.

	- To do that, go back to "ReviewSerializer" class, if you remove the 'prodcut' from the array of "fields" and in then in the request body you do NOT assign a product_id then you will get an error saying "product_id cannot be null"
	- This serializer class methods for creating/updating reviews and while creating a review it will take all the values defined in the field array and use them to set the values of Review object.
	- ANd now here we do NOT have product_id field (Removed it)

	- PROBLEM SOLVING:
	- In our "ReviewViewSet" class we have access to url parameters. and we can read the product_id from the url and using a context object we can pass it to the Serializer.
	- We use "context" object to provide additional data to the serializer.
	- So we will override "get_serializer_context()" method and return dictionary.
	- Our urls has two parameters "product_pk" contains product_id and "pk" for review_id.

	def get_serializer_context(self):
        return {'product_id': self.kwargs['product_id']}

    - Now that we have access to product_id, now we will override the create method in our serializer class of review.

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)

    - Now using this we can successfully create a review without assigning the product_id

    - But now a problem remains:
    - all the reviews that have been created so far are showing for every product even though they do NOT belong to them.
    - this is because in "ReviewViewSet" class we have set our queryset to all.

    queryset = Review.objects.all()

    - So all reviews are returned no matter what product we are on.
    - here instead of setting "queryset" attribute we will override "get_queryset" method.

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    - Now this will solve that problem.


# Filtering:
	- Currenlty when we hit "products" endpoint we get all products from our database.
	- What if we want to filter these products, (e.g., by a specific collection).
	- We should be able to pass a query string parameter like "collection_id" (?collection_id=1) and then we should only see products in collection 1.
	- In "ProductViewSet" we have a query set to get all the products

	queryset = Product.objects.all()

	- So again here instead of setting "queryset" attribute we will override "get_queryset" method.

	def get_queryset(self):
        queryset = Product.objects.all()
        collection_id = self.request.query_params['collection_id']
        if collection_id is not None:
            queryset = queryset.filter(collection_id=collection_id)
        return queryset

    - "query_params" is a dictionary.
    -  By the above we get following error:

    - `basename` argument not specified, and could not automatically determine the name from the viewset, as it does not have a `.queryset` attribute.

    - As we have removed "queryset" attribute from our class django_rest_framework is unable to figure out the "basename"
    - We defined "basename" in the urls.py while registering the route.
    - This "basename" is used to generate the name of our url patterns.
    - By default "djangoRestFramework" uses the queryset attribute to figure out the basename.
    - But now we have deleted queryset attribute and have a method django_rest_framework cannot figure what the "basename" should be called based on the logic we defined in that method.
    - So, for "products" we have to explicitly define the "basename"

    router.register('products', views.ProductViewSet, basename='products')

    - With this we will have 2 urlpatterns ==== "products-list" and "products-detail" ---- "products" is just a prefix.

    - Now we get another error:  "MultiValueDictKeyError at /store/products/   collection_id" 
    - Here, if you pass a "collection_id" as query_parameters the error will go away.
    - Access you dictionary key "collection_id" using "get()" method. ANd the error will go away.

    collection_id = self.request.query_params.get('collection_id')



# Generic Filtering:
	- What if we want to filter product by some other field, we will need to use more complicated code.
	- There is a third party library called "django-filter", there we can filter any model by any field. 

	- pip install django-filter                     (For installing globally)
	- pipenv install django-filter                  (For installing only in venv)

	- Also add it in the list of installed apps.   ('django_filters')   -------- Name of the app differ from name of the library  (django-filter >>>>>> django_filters)
	
	from django_filters.rest_framework import DjangoFilterBackend

	- 'DjangoFilterBackend' gives us generic filtering
	- Add the followin attribute to your class.

	filter_backends = [DjangoFilterBackend]

	- With this backend all we have to do is specifr what field we want to use for filtering.

	filterset_fields = ['collection_id']

	- Now with that you do NOT need all that logic that you have defined in the previous lecture for "collection_id".
	- With this filtering, we can filter our products using query_parameters as well as we get a button "Filters" where we can easily select a collection.
	- Want to filter using another field, just pass it in "filterset_fields" and it willbe done.

	- When we pass "unit_price" as a field for filtering, it will ask us to give us the exact amount for which you want to finf products.
	- Bit we want to filter our ptoducts for a price range not just a single price.
	- This is where we will need to use a custom filter (will not be taught in this course)
	- Look at the documentation of django-filter library.
	- There you can find all the details about creating a custom filter.

	- Add a new file "filters.py" in store app.
	
	from django_filters.rest_framework import FilterSet

	- Create a class "ProductFilter" which should inherit "FilterSet".
	- Add another class Meta where you will define model and fields for the filtering.
	- fields will be a dictionary, and there, for each field we can specify how the filtering should be done.
	- 'exact' for exact filtering
	- For a range, use less than an greate than ['lt', 'gt']
	- A special language that this library understands.
	- For more details, look at the documentation

	- Now in our "ProductViewSet" class, instead of using, 'filterset_fields' we will use 'serializer_class' and set this equal to our filter class.


# Searching:
	- If you want to find product by title or description, you should use Searching.
	- Searching is for text-based fields.

	from rest_framework.filters import SearchFilter

	- In the "filter_backends" array add this "SearchFilter"

	filter_backends = [DjangoFilterBackend, SearchFilter

	- Add another array "search_fields" and set this equal to the list of fields you want to use for Searching

	search_fields = ['name', 'description'] 

	- We can also reference field of the related classes using double underscore 'collection__title'
	- Now in our browsableApi, in filter button we also have a search field.
	- This search is case-sensitive.


# Sorting:
	from rest_framework.filters import OrderingFilter

	- import from the same module as before. Add this in "filter_backends" array.

	filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

	- Add another array "ordering_fields" and set this equal to the list of fields you want to use for Sorting.

	ordering_fields = ['unit_price', 'last_updated']

	- You will get some ways of sorting your data in filter.
	- You can also modify your queryset for sorting here.

	- The queryset for ascending unit_price is "?ordering=unit_price"
	- The queryset for descending unit_price is "?ordering=-unit_price"

	- This will not let you sort your data a with more than one criteria.
	- So for that you can modify your url yourself.    ----------- '?ordering=-unit_price,last_update'

	- What is interesting about above query parameter is, currently we are not returning last_update from our API
	- And even though we are NOT returning it here, we can still use it for sorting data.


# Pagination:
	from rest_framework.pagination import PageNumberPagination

	- Using this class we can paginate our data using page number.
	- Add an attribute in your class 'pagination_class' and set this equal to  "PageNumberPagination"

	pagination_class = PageNumberPagination

	- Now we need to specify our pagesize.
	- For that we need to go to "setting.py"
	- In the settings of "REST_FRAMEWORK" set page size to 10

	REST_FRAMEWORK = {
    	'COERCE_DECIMAL_TO_STRING': False,
    	'PAGE_SIZE': 10,
	}

	- Now if you refresh your page, you will see a slightly different result.
	- Instead of an array of object, we get an object with some properties.
	- "count"  ---- for total no of results
	- "next"   ---- link to the next page   	(null in case of last page)
	- "previous" -- link to the previous page   (null in case of first page)
	- "results"  -- an array of our results.

	- We have set this pagination in our "ProductViewSet" class only, it will not be in other endpounts.
	- If you want to set it globally modify REST_FRAMEWORK dict in settings.py and add this:
	'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination'

	REST_FRAMEWORK = {
    	'COERCE_DECIMAL_TO_STRING': False,
    	'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    	'PAGE_SIZE': 10,
	}

	- With this you will not need to set this per viewset, it will be set globally for every class.

	- Now we have another pagination class called "LimitOffsetPagination", so instead of using the page number we use a limit and an offset value.
	- Change pagination class to "LimitOffsetPagination"

	REST_FRAMEWORK = {
		'COERCE_DECIMAL_TO_STRING': False,
    	'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    	'PAGE_SIZE': 10,
	}

	- Now in our query set parameter, we have limit and offset instead of page number.

	- If we do NOT want to apply this globally and remove 'DEFAULT_PAGINATION_CLASS' from "settings.py" we get following warning:

	?: (rest_framework.W001) You have specified a default PAGE_SIZE pagination rest_framework setting, without specifying also a DEFAULT_PAGINATION_CLASS.
        HINT: The default for DEFAULT_PAGINATION_CLASS is None. In previous versions this was PageNumberPagination. If you wish to define PAGE_SIZE globally whilst defining pagination_class on a per-view basis you may silence this check.

    - This is because we remove 'DEFAULT_PAGINATION_CLASS' and left the 'PAGE_SIZE' there.
    - We can either supppress this warning oe create a custom pagination class and set page size there. We will create a custom class.

    - Add a new file , "pagination.py" ---- import "PageNumberPagination"
    
    from rest_framework.pagination import PageNumberPagination
    
    - Create a custom class "DefaultPagination" which will inherit from "PageNumberPagination"
    - And there set page_size = 10

    class DefaultPagination(PageNumberPagination):
    	page_size = 10

    - Remove 'PAGE_SIZE' from 'settings.py'
    - And in "ProductViewSet" class in change "pagination_class" to this custom class.

    pagination_class = DefaultPagination
    




 