from django.urls import path, register_converter

from .views import (
    AboutPage,
    AddProductPage,
    CatalogHome,
    DeleteProductPage,
    ProductCategory,
    ShowProduct,
    TagProductList,
    UpdateProductPage,
    add_comment,
    set_reaction,
)


class SignedIntConverter:
    regex = '-?\\d+'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return str(value)


register_converter(SignedIntConverter, 'int')

urlpatterns = [
    path('', CatalogHome.as_view(), name='home'),
    path('about/', AboutPage.as_view(), name='about'),
    path('addpage/', AddProductPage.as_view(), name='add_page'),
    path('product/<slug:product_slug>/', ShowProduct.as_view(), name='product'),
    path('edit/<slug:product_slug>/', UpdateProductPage.as_view(), name='edit_page'),
    path('delete/<slug:product_slug>/', DeleteProductPage.as_view(), name='delete_page'),
    path('category/<slug:cat_slug>/', ProductCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', TagProductList.as_view(), name='tag'),
    path('product/<slug:product_slug>/comment/', add_comment, name='add_comment'),
    path('product/<slug:product_slug>/reaction/<int:value>/', set_reaction, name='set_reaction'),
]