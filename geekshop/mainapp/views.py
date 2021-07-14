from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import ProductCategory, Product
from basketapp.models import Basket
import random


class ProductsView(ListView):
    model = Product
    ordering = 'price'
    context_object_name = 'products'
    paginate_by = 3

    def get_template_names(self):
        if 'pk' in self.kwargs:
            return ['mainapp/products_list.html']
        else:
            return ['mainapp/products.html']

    # def get_basket(self):
    #     if self.request.user.is_authenticated:
    #         return Basket.objects.filter(user=self.request.user)
    #     else:
    #         return []

    def get_hot_product(self):
        return random.sample(list(self.get_queryset()), 1)[0]

    def get_same_products(self,):
        hot_product = self.get_hot_product()
        same_products = self.get_queryset().filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
        return same_products

    def get_queryset(self):
        queryset = super(ProductsView, self).get_queryset()
        if 'pk' in self.kwargs:
            if self.kwargs['pk'] == 0:
                return queryset
            else:
                queryset = queryset.filter(category_id__pk=self.kwargs['pk'])
                return queryset
        else:
            return queryset

    def get_category(self):
        if 'pk' in self.kwargs:
            if self.kwargs['pk'] == 0:
                category = {
                    'pk': 0,
                    'name': 'все'}
            else:
                category = get_object_or_404(ProductCategory, pk=self.kwargs['pk'])
            return category

    def get_context_data(self, **kwargs):
        context = super(ProductsView, self).get_context_data(**kwargs)
        links_menu = ProductCategory.objects.all()
        # context['basket'] = self.get_basket()
        context['title'] = 'продукты'
        context['links_menu'] = links_menu
        context['category'] = self.get_category()
        context['hot_product'] = self.get_hot_product()
        context['same_products'] = self.get_same_products()
        return context


class ProductView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'mainapp/product.html'

    # def get_basket(self):
    #     if self.request.user.is_authenticated:
    #         return Basket.objects.filter(user=self.request.user)
    #     else:
    #         return []

    def get_context_data(self, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)
        links_menu = ProductCategory.objects.all()
        # context['basket'] = self.get_basket()
        context['title'] = 'продукт'
        context['links_menu'] = links_menu

        return context
