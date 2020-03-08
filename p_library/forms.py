from django import forms
from p_library.models import Book, Author


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        labels = {
            'title': 'Название  книги',
            'description': 'Описание книги',
            'year_release': 'Год релиза',
            'copy_count':'Число копий',
            'price': 'Цена',
            'author': 'Автор',
            'friend': 'Друг'
        }
        help_text = {'title': 'Должно быть уникальным',}

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'
        labels = {
            'full_name': 'Полное имя автора',
            'birth_year': 'Год рождения',
            'country': 'Страна автора'
        }
        widgets = {
            'country': forms.Textarea
        }

    
