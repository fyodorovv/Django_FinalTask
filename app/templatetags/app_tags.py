from django import template
from django.db.models import Count

from app.models import Basket, Category, Product
from app.utils import menu

register = template.Library()


@register.inclusion_tag('app/list_categories.html')
def show_categories():
    cats = Category.objects.all()
    # cats = Category.objects.annotate(
    #     total=Count("category")).filter(total__gt=0)
    return {'cats': cats}


@register.inclusion_tag('app/list_carousel.html')
def carousel_list():
    carousel_items = Product.objects.filter(is_promotion=True)[:3]
    return {'carousel_items': carousel_items}


@register.simple_tag
def get_menu():
    return menu


@register.simple_tag(takes_context=True)
def get_basket_count(context):
    request = context['request']
    user = request.user
    if user.is_authenticated:
        return Basket.objects.filter(user=user).count()
    return 0
