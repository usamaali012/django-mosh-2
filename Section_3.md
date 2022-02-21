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
	- There are situations where generic views might not work for us.
	- 