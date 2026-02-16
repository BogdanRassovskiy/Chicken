from django import forms
from django.contrib import admin

from .models import Category, Product


def _work_to_bool(value):
    if value is None:
        return False
    return str(value).strip().lower() in {'1', 'true', 'yes', 'on'}


class ProductAdminForm(forms.ModelForm):
    work = forms.BooleanField(label='Включен', required=False)
    img = forms.FileField(label='Изображение', required=False)
    cat_id = forms.ChoiceField(label='Category', required=False)

    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.order_by('name', 'id').values_list('id', 'name')
        choices = [('', '---------')]
        for category_id, category_name in categories:
            label = category_name or category_id
            choices.append((category_id, label))
        self.fields['cat_id'].choices = choices
        if self.instance and self.instance.pk:
            self.fields['cat_id'].initial = self.instance.cat_id
            self.fields['work'].initial = _work_to_bool(self.instance.work)

    def clean_work(self):
        return '1' if self.cleaned_data.get('work') else '0'

    def clean_img(self):
        uploaded_file = self.cleaned_data.get('img')
        if hasattr(uploaded_file, 'read'):
            return uploaded_file.read()
        if isinstance(uploaded_file, (bytes, bytearray, memoryview)):
            return bytes(uploaded_file)
        if self.instance and self.instance.pk:
            return self.instance.img
        return None

    def clean_cat_id(self):
        value = self.cleaned_data.get('cat_id')
        return value or None


class CategoryAdminForm(forms.ModelForm):
    cat_id = forms.ChoiceField(label='Category', required=False)
    work = forms.BooleanField(label='Включен', required=False)
    img = forms.FileField(label='Изображение', required=False)

    class Meta:
        model = Category
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.order_by('name', 'id').values_list('id', 'name')
        choices = [('', '---------')]
        current_id = self.instance.id if self.instance and self.instance.pk else None
        for category_id, category_name in categories:
            if current_id and category_id == current_id:
                continue
            label = category_name or category_id
            choices.append((category_id, label))
        self.fields['cat_id'].choices = choices
        if self.instance and self.instance.pk:
            self.fields['cat_id'].initial = self.instance.cat_id
            self.fields['work'].initial = _work_to_bool(self.instance.work)

    def clean_cat_id(self):
        value = self.cleaned_data.get('cat_id')
        return value or None

    def clean_work(self):
        return '1' if self.cleaned_data.get('work') else '0'

    def clean_img(self):
        uploaded_file = self.cleaned_data.get('img')
        if hasattr(uploaded_file, 'read'):
            return uploaded_file.read()
        if isinstance(uploaded_file, (bytes, bytearray, memoryview)):
            return bytes(uploaded_file)
        if self.instance and self.instance.pk:
            return self.instance.img
        return None


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ('id', 'name', 'name_uz', 'price', 'work', 'cat_id')
    search_fields = ('id', 'name', 'name_uz')
    list_filter = ('work',)
    fields = ('id', 'name', 'name_uz', 'rev', 'rev_uz', 'work', 'price', 'img', 'cat_id')
    readonly_fields = ('id',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    list_display = ('id', 'name', 'name_uz', 'work', 'cat_id')
    search_fields = ('id', 'name', 'name_uz')
    list_filter = ('work',)
    fields = ('id', 'name', 'name_uz', 'work', 'cat_id', 'img')
    readonly_fields = ('id',)
