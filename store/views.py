from random import randint

from django.shortcuts import render
from .models import *
from django.views.generic import ListView, DetailView
from .forms import ReviewForm


# Create your views here.

#  Класс для главной страницы сайта
class ProductList(ListView):
    model = Product
    context_object_name = 'categories'
    extra_context = {
        'title': 'Онлайн магазин TOTEMBO'
    }
    template_name = 'store/product_list.html'

    #  Метод что бы перназначить вывод что бы получать подкатегории определённой категории
    def get_queryset(self):
        categories = Category.objects.filter(parent=None)
        return categories


class CategoryView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'store/category_page.html'

    # Метод для вывода данных по сортирвке
    def get_queryset(self):
        sort_field = self.request.GET.get('sort')
        type_field = self.request.GET.get('type')
        if type_field:  # Если получили что то в type
            products = Product.objects.filter(category__slug=type_field)
            return products
        main_category = Category.objects.get(slug=self.kwargs['slug'])  # получаем главную категорию
        subcategories = main_category.subcategories.all()  # Получаем все подкатегории
        products = Product.objects.filter(category__in=subcategories)  # Получаем все продукты всех подкатегорий

        if sort_field:
            products = products.order_by(sort_field)
        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        main_category = Category.objects.get(slug=self.kwargs['slug'])
        context['category'] = main_category
        context['title'] = f'Категория: {main_category.title}'
        return context


# Вьюшка для страницы Детали Товара
class ProductDetail(DetailView):  # product_detail.html
    model = Product
    context_object_name = 'product'

    # Метод для шапки страницы
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        product = Product.objects.get(slug=self.kwargs['slug'])
        context['title'] = f'{product.category} {product.title}'

        products = Product.objects.all()  # ['hublot', 'rolex']
        data = []
        for i in range(4):
            random_index = randint(0, len(products)-1)
            p = products[random_index]
            if p not in data:
                data.append(p)
            context['products'] = data

        if self.request.user.is_authenticated:
            context['review_form'] = ReviewForm()

        return context
