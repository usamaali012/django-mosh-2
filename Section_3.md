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