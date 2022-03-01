from django.urls import path
from . import views

# URLConf
urlpatterns = [
    # For class based views
    path('products/', views.ProductList.as_view()),
    path('products/<int:pk>/', views.ProductDetail.as_view()),
    path('collections/', views.CollectionList.as_view()),
    path('collections/<int:pk>/', views.CollectionDetail.as_view(), name='collection-detail'),

    # For Function based views
    # path('products/', views.product_list),
    # path('products/<int:id>/', views.product_details),
    # path('collections/', views.collection_list),
    # path('collections/<int:pk>/', views.collection_detail, name='collection-detail'),
]
