from .import views
# -------------------------------------------Nested Routers---------------------------------------------------
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')

urlpatterns = router.urls + products_router.urls


# -------------------------------------------Default Router---------------------------------------------------
# from rest_framework.routers import DefaultRouter
# router = DefaultRouter()
# router.register('products', views.ProductViewSet)
# router.register('collections', views.CollectionViewSet)

# urlpatterns = router.urls

# pprint(router.urls)
# # router.urls = [
# #     <URLPattern '^products/$' [name='product-list']>,
# #     <URLPattern '^products\.(?P<format>[a-z0-9]+)/?$' [name='product-list']>,
# #     <URLPattern '^products/(?P<pk>[^/.]+)/$' [name='product-detail']>,
# #     <URLPattern '^products/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$' [name='product-detail']>,
# #     <URLPattern '^collections/$' [name='collection-list']>,
# #     <URLPattern '^collections\.(?P<format>[a-z0-9]+)/?$' [name='collection-list']>,
# #     <URLPattern '^collections/(?P<pk>[^/.]+)/$' [name='collection-detail']>,
# #     <URLPattern '^collections/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$' [name='collection-detail']>,
# #     <URLPattern '^$' [name='api-root']>,
# #     <URLPattern '^\.(?P<format>[a-z0-9]+)/?$' [name='api-root']>
# #     ]



# -------------------------------------------Simpe Router-----------------------------------------------------
# from rest_framework.routers import SimpleRouter
# router = SimpleRouter()
# router.register('products', views.ProductViewSet)
# router.register('collections', views.CollectionViewSet)

# urlpatterns = router.urls

# pprint(router.urls)
# # router.urls = [
# #     <URLPattern '^products/$' [name='product-list']>,
# #     <URLPattern '^products/(?P<pk>[^/.]+)/$' [name='product-detail']>,
# #     <URLPattern '^collections/$' [name='collection-list']>,
# #     <URLPattern '^collections/(?P<pk>[^/.]+)/$' [name='collection-detail']>
# #     ]



# # If you have more URLs than defined by router.urls, you can use the following syntax:----------------------
# from django.urls import path, include
# urlpatterns = [
#     path('', include(router.urls)),
#     # Here define your URL patterns which are not defined by router.urls
# ]


# -------------------------------------------OLD CONFIGURATION------------------------------------------------
# from django.urls import path
# urlpatterns = [
# #                       -------------------For class based views--------------------------
#     # path('products/', views.ProductList.as_view()),
#     # path('products/<int:pk>/', views.ProductDetail.as_view()),
#     # path('collections/', views.CollectionList.as_view()),
#     # path('collections/<int:pk>/', views.CollectionDetail.as_view(), name='collection-detail'),

# #                       ---------------------For Function based views-----------------------
#     # path('products/', views.product_list),
#     # path('products/<int:id>/', views.product_details),
#     # path('collections/', views.collection_list),
#     # path('collections/<int:pk>/', views.collection_detail, name='collection-detail'),
# ]
