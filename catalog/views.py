from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from .forms import AddProductForm, CommentForm
from .mixins import AuthorRequiredMixin, DataMixin
from .models import Category, Comment, Reaction, TagProduct, TimberProduct


class CatalogHome(DataMixin, ListView):
    template_name = 'catalog/index.html'
    context_object_name = 'products'
    title_page = 'Timber Market — каталог пиломатериалов'
    cat_selected = 0
    paginate_by = 3

    def get_queryset(self):
        return (
            TimberProduct.published
            .select_related('cat', 'author', 'supplier')
            .prefetch_related('tags')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=self.title_page, cat_selected=0)


class AboutPage(DataMixin, TemplateView):
    template_name = 'catalog/about.html'
    title_page = 'О компании Timber Market'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=self.title_page)


class ShowProduct(DataMixin, DetailView):
    model = TimberProduct
    template_name = 'catalog/product.html'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'

    def get_queryset(self):
        return (
            TimberProduct.published
            .select_related('cat', 'author', 'supplier')
            .prefetch_related('tags')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object

        comments = (
            Comment.objects
            .filter(product=product, is_active=True)
            .select_related('author')
            .order_by('time_create')
        )

        likes_count = product.reactions.filter(value=Reaction.Value.LIKE).count()
        dislikes_count = product.reactions.filter(value=Reaction.Value.DISLIKE).count()

        user_reaction = None
        if self.request.user.is_authenticated:
            reaction = product.reactions.filter(user=self.request.user).first()
            if reaction:
                user_reaction = reaction.value

        context['comments'] = comments
        context['comment_form'] = CommentForm()
        context['likes_count'] = likes_count
        context['dislikes_count'] = dislikes_count
        context['user_reaction'] = user_reaction

        return self.get_mixin_context(context, title=product.title, cat_selected=product.cat_id)


class AddProductPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddProductForm
    template_name = 'catalog/addpage.html'
    title_page = 'Добавить материал'
    login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Карточка пиломатериала успешно создана.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=self.title_page)


class UpdateProductPage(LoginRequiredMixin, AuthorRequiredMixin, DataMixin, UpdateView):
    model = TimberProduct
    form_class = AddProductForm
    template_name = 'catalog/addpage.html'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'
    title_page = 'Редактировать материал'
    login_url = reverse_lazy('users:login')

    def get_queryset(self):
        return TimberProduct.objects.select_related('author', 'cat', 'supplier').prefetch_related('tags')

    def form_valid(self, form):
        messages.success(self.request, 'Карточка пиломатериала успешно обновлена.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=self.title_page)


class DeleteProductPage(LoginRequiredMixin, AuthorRequiredMixin, DataMixin, DeleteView):
    model = TimberProduct
    template_name = 'catalog/delete_confirm.html'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'
    success_url = reverse_lazy('home')
    title_page = 'Удалить материал'
    login_url = reverse_lazy('users:login')

    def get_queryset(self):
        return TimberProduct.objects.select_related('author', 'cat')

    def form_valid(self, form):
        messages.success(self.request, 'Карточка пиломатериала удалена.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=self.title_page)


class ProductCategory(DataMixin, ListView):
    template_name = 'catalog/index.html'
    context_object_name = 'products'
    paginate_by = 3
    allow_empty = False

    def get_queryset(self):
        self.category = get_object_or_404(
            Category.objects.annotate(
                total=Count(
                    'products',
                    filter=Q(products__is_published=TimberProduct.Status.PUBLISHED),
                )
            ).filter(total__gt=0),
            slug=self.kwargs['cat_slug'],
        )

        return (
            TimberProduct.published
            .filter(cat=self.category)
            .select_related('cat', 'author', 'supplier')
            .prefetch_related('tags')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context,
            title=f'Категория: {self.category.name}',
            cat_selected=self.category.pk,
        )


class TagProductList(DataMixin, ListView):
    template_name = 'catalog/index.html'
    context_object_name = 'products'
    paginate_by = 3
    allow_empty = False

    def get_queryset(self):
        self.tag = get_object_or_404(
            TagProduct.objects.annotate(
                total=Count(
                    'products',
                    filter=Q(products__is_published=TimberProduct.Status.PUBLISHED),
                )
            ).filter(total__gt=0),
            slug=self.kwargs['tag_slug'],
        )

        return (
            TimberProduct.published
            .filter(tags=self.tag)
            .select_related('cat', 'author', 'supplier')
            .prefetch_related('tags')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context,
            title=f'Тег: {self.tag.tag}',
            cat_selected=None,
        )


@login_required
def add_comment(request, product_slug):
    product = get_object_or_404(TimberProduct.published, slug=product_slug)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.author = request.user
            comment.save()
            messages.success(request, 'Комментарий добавлен.')
        else:
            messages.error(request, 'Комментарий не был добавлен. Проверьте текст.')

    return redirect(product.get_absolute_url())


@login_required
def set_reaction(request, product_slug, value):
    product = get_object_or_404(TimberProduct.published, slug=product_slug)

    if request.method != 'POST':
        return redirect(product.get_absolute_url())

    if value not in (Reaction.Value.LIKE, Reaction.Value.DISLIKE):
        messages.error(request, 'Некорректная реакция.')
        return redirect(product.get_absolute_url())

    reaction, created = Reaction.objects.get_or_create(
        product=product,
        user=request.user,
        defaults={'value': value},
    )

    if not created:
        if reaction.value == value:
            reaction.delete()
            messages.info(request, 'Реакция удалена.')
        else:
            reaction.value = value
            reaction.save(update_fields=['value'])
            messages.success(request, 'Реакция изменена.')
    else:
        messages.success(request, 'Реакция добавлена.')

    return redirect(product.get_absolute_url())