from xml.etree.ElementInclude import include
from django.urls import path
from rest_framework.routers import SimpleRouter, DefaultRouter
from .import views
# from pprint import pprint

# DefaultRouter
router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)

urlpatterns = router.urls

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



# # SimpleRouter
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



# # If you have more URLs than defined by router.urls, you can use the following syntax:
# urlpatterns = [
#     path('', include(router.urls)),
#     # Here define your URL patterns which are not defined by router.urls
# ]



# OLD CONFIGURATION
# URLConf
# urlpatterns = [
#     # For class based views
#     # path('products/', views.ProductList.as_view()),
#     # path('products/<int:pk>/', views.ProductDetail.as_view()),
#     # path('collections/', views.CollectionList.as_view()),
#     # path('collections/<int:pk>/', views.CollectionDetail.as_view(), name='collection-detail'),

#     # For Function based views
#     # path('products/', views.product_list),
#     # path('products/<int:id>/', views.product_details),
#     # path('collections/', views.collection_list),
#     # path('collections/<int:pk>/', views.collection_detail, name='collection-detail'),
# ]
