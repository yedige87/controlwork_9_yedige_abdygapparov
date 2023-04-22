from django import forms

from photos.models import Photo


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('image', 'description')
        labels = {
            'image': 'Фотография',
            'description': 'Описание фото',
        }

class SearchForm(forms.Form):
    search = forms.CharField(max_length=20, required=False, label='Найти')


class CommentForm(forms.Form):
    text = forms.CharField(max_length=200, required=True, label='', widget=forms.TextInput(attrs={'placeholder': 'Введите свой комментарий'}))