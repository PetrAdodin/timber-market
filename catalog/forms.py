from django import forms
from django.core.exceptions import ValidationError

from .models import Comment, Supplier, TimberProduct


class AddProductForm(forms.ModelForm):
    class Meta:
        model = TimberProduct
        fields = [
            'title',
            'slug',
            'content',
            'photo',
            'wood_type',
            'size',
            'grade',
            'price',
            'is_published',
            'cat',
            'supplier',
            'tags',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: Доска обрезная 50×150×6000 мм',
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'doska-obreznaya-50x150',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Опишите материал, назначение, преимущества и область применения',
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control',
            }),
            'wood_type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Сосна, ель, лиственница, дуб',
            }),
            'size': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '50×150×6000 мм',
            }),
            'grade': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '1 сорт, 2 сорт, Экстра',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.01',
                'placeholder': '12500.00',
            }),
            'is_published': forms.Select(attrs={
                'class': 'form-control',
            }),
            'cat': forms.Select(attrs={
                'class': 'form-control',
            }),
            'supplier': forms.Select(attrs={
                'class': 'form-control',
            }),
            'tags': forms.SelectMultiple(attrs={
                'class': 'form-control form-control-multiple',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['cat'].empty_label = 'Выберите категорию'
        self.fields['supplier'].empty_label = 'Поставщик не указан'

        current_supplier_id = self.instance.supplier_id if self.instance and self.instance.pk else None
        used_supplier_ids = TimberProduct.objects.exclude(pk=self.instance.pk).exclude(
            supplier__isnull=True
        ).values_list('supplier_id', flat=True)

        supplier_queryset = Supplier.objects.exclude(id__in=used_supplier_ids)
        if current_supplier_id:
            supplier_queryset = Supplier.objects.filter(id=current_supplier_id) | supplier_queryset

        self.fields['supplier'].queryset = supplier_queryset.distinct()

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title.strip()) < 5:
            raise ValidationError('Название материала должно быть не короче 5 символов.')
        return title

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        queryset = TimberProduct.objects.filter(slug=slug)

        if self.instance and self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise ValidationError('Карточка с таким slug уже существует.')
        return slug

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise ValidationError('Цена не может быть отрицательной.')
        return price


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Напишите комментарий о материале',
            }),
        }
        labels = {
            'text': 'Комментарий',
        }

    def clean_text(self):
        text = self.cleaned_data['text']
        if len(text.strip()) < 3:
            raise ValidationError('Комментарий должен содержать не менее 3 символов.')
        return text