from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import UserPassesTestMixin


class DataMixin:
    paginate_by = 3

    menu = [
        {'title': 'Главная', 'url_name': 'home'},
        {'title': 'О компании', 'url_name': 'about'},
        {'title': 'Добавить материал', 'url_name': 'add_page'},
    ]

    title_page = None
    cat_selected = None

    def get_mixin_context(self, context, **kwargs):
        context['menu'] = self.menu
        context['title'] = kwargs.get('title', self.title_page)
        context['cat_selected'] = kwargs.get('cat_selected', self.cat_selected)
        return context


class AuthorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        user = self.request.user
        return user.is_superuser or obj.author == user

    def handle_no_permission(self):
        raise PermissionDenied('Редактировать или удалять карточку может только автор или суперпользователь.')