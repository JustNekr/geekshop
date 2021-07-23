from django.urls import path
from django.views.decorators.cache import cache_page

from .views import ProductsView, ProductView

app_name = 'mainapp'

urlpatterns = [
    path('', cache_page(3600)(ProductsView.as_view()), name='products'),
    path('category/<int:pk>/', cache_page(3600)(ProductsView.as_view()), name='category'),
    # path('category/<int:pk>/page/<int:page>', ProductsView.as_view(), name='page'),
    path('product/<int:pk>/', cache_page(3600)(ProductView.as_view()), name='product'),
]
