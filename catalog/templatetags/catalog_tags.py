from django import template
from django.db.models import Count, Q

from catalog.models import Category, TagProduct, TimberProduct

register = template.Library()


@register.inclusion_tag('catalog/list_categories.html')
def show_categories(cat_selected=0):
    categories = (
        Category.objects
        .annotate(
            total=Count(
                'products',
                filter=Q(products__is_published=TimberProduct.Status.PUBLISHED),
            )
        )
        .filter(total__gt=0)
        .order_by('name')
    )
    return {
        'categories': categories,
        'cat_selected': cat_selected,
    }


@register.inclusion_tag('catalog/list_tags.html')
def show_all_tags():
    tags = (
        TagProduct.objects
        .annotate(
            total=Count(
                'products',
                filter=Q(products__is_published=TimberProduct.Status.PUBLISHED),
            )
        )
        .filter(total__gt=0)
        .order_by('tag')
    )
    return {
        'tags': tags,
    }