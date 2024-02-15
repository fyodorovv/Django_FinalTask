from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, ListView, DetailView
from .utils import DataMixin
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from app.forms import AddProductForm, LoginUserForm, RegisterUserForm

from .models import Product, Basket, Category


class HomePage(DataMixin, ListView):
    template_name = 'app/index.html'
    context_object_name = 'products'
    title_page = 'Главная страница'

    def get_queryset(self):
        return Product.published.all()[:3]


class ProductCategory(DataMixin, ListView):
    template_name = 'app/index.html'
    context_object_name = 'products'
    allow_empty = True

    def get_queryset(self):
        return Product.published.filter(category__slug=self.kwargs['category_slug']).select_related("category")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = context['products'][0].category
        return self.get_mixin_context(context, title=category.name)


class ShowProduct(DataMixin, DetailView):
    template_name = 'app/product.html'
    context_object_name = 'product'
    slug_url_kwarg = 'product_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['product'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Product.published, slug=self.kwargs['product_slug'])


class AddProduct(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddProductForm
    template_name = 'app/addproduct.html'
    title_page = 'Добавление продукта'


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'app/login.html'
    extra_context = {'title': 'Авторизация'}

    def logout_user(request):
        logout(request)
        return HttpResponseRedirect(reverse('login'))


class BasketView(LoginRequiredMixin, DataMixin, ListView):
    template_name = 'app/basket.html'
    context_object_name = 'basket'
    title_page = 'Корзина'

    def get_queryset(self):
        return Basket.objects.filter(user=self.request.user)

    def add_to_basket(request, product_id):
        product = get_object_or_404(Product, id=product_id)
        basket = Basket.objects.get_or_create(
            user=request.user, product=product)[0]
        basket.quantity += 1
        basket.save()
        return redirect('product', product_slug=product.slug)

    def remove_from_basket(request, product_id):
        product = get_object_or_404(Product, id=product_id)
        basket = Basket.objects.get(user=request.user, product=product)
        basket.delete()
        return redirect('basket')

    def add_product(request, product_id):
        product = get_object_or_404(Product, id=product_id)
        basket = Basket.objects.get(
            user=request.user, product=product)
        basket.quantity += 1
        basket.save()
        return redirect('basket')

    def remove_product(request, product_id):
        product = get_object_or_404(Product, id=product_id)
        basket = Basket.objects.get(
            user=request.user, product=product)
        basket.quantity -= 1
        if basket.quantity < 1:
            basket.delete()
        else:
            basket.save()
        return redirect('basket')


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'app/register.html'
    extra_context = {'title': 'Регистрация'}
    success_url = '/login'


@login_required
def about(request):
    return HttpResponse("<h1>О нас</h1><p>Это страница о нас</p><p><a href='/'>На главную</a></p>")
