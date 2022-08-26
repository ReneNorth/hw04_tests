from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')
        labels = {
            'text': 'Текст вашего поста',
            'group': 'Группа',
        }
        help_texts = {
            'text': 'Начните писать! Вдохновение придёт со временем.',
            'group': 'Пост будет относится к выбранной группе',
        }

    def clean_text(self):
        data = self.cleaned_data['text']
        return data
