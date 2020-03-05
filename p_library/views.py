from django.urls import reverse, reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import ContextMixin
from django.views.generic.edit import ProcessFormView
from django.views.generic.edit import (
    CreateView, UpdateView, DeleteView,
)
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from p_library.models import Author, Book, Friend
from p_library.forms import BookForm
# Create your views here.

###################### Примеси и вспомогательные классы ###############################


class AuthorListMixin(ContextMixin):
    """Примесь,добавляющая в контекст список авторов"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authors'] = Author.objects.order_by('full_name')
        return context


class BookMixin(ContextMixin):
    """Примесь, добавляющая в контекст автора, которому принадлежить книга"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author_by'] = Book.objects.get(
            pk=self.kwargs['book_id']).author
        return context


class BookEditMixin(AuthorListMixin):
    """Примесь, добавляющая в контекст номер страницы
    в таблице, список авторов и книгу, принадлежащую определенному автору"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pn'] = self.request.GET.get('page', 1)
        return context


class BookEditView(ProcessFormView):
    """Добавляет GET-параметр страницы к url в случае успеха при изменении формы"""

    def post(self, request, *args, **kwargs):
        pn = self.request.GET.get('page', 1)
        self.success_url = self.success_url + "?page=" + pn
        return super().post(self, request, *args, **kwargs)


###################### Основные контроллеры ###############################

class BookListView(ListView, AuthorListMixin):
    """Контроллер списка книг"""

    template_name = 'books_list.html'
    paginate_by = 2
    author_by = None

    def get(self, request, *args, **kwargs):
        if self.kwargs['author_id'] == None:
            self.author_by = Author.objects.first()
        else:
            self.author_by = Author.objects.get(pk=self.kwargs['author_id'])
        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author_by'] = self.author_by
        return context

    def get_queryset(self):
        return Book.objects.filter(author=self.author_by).order_by('title')


class BookDetailView(DetailView, BookEditMixin, BookMixin):
    template_name = 'book_detail.html'
    model = Book
    pk_url_kwarg = 'book_id'

    

class BookCreateView(SuccessMessageMixin, CreateView, BookEditMixin):
    template_name = 'book_add.html'
    model = Book
    form_class = BookForm
    success_message = 'Книга успешно добавлена'
    
    def get(self, request, *args, **kwargs):
        if self.kwargs['author_id'] != None:
            self.initial['author'] = Author.objects.get(
                pk=self.kwargs['author_id'])
        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author_by'] = Author.objects.get(pk=self.kwargs['author_id'])
        return context

    def post(self, request, *args, **kwargs):
        self.success_url = reverse('p_library:books_list', kwargs={
            'author_id': Author.objects.get(pk=self.kwargs['author_id']).id})
        return super().post(self, request, *args, **kwargs)


class BookUpdateView(SuccessMessageMixin, UpdateView, BookEditView, BookEditMixin, BookMixin):
    template_name = 'book_update.html'
    model = Book
    form_class = BookForm
    pk_url_kwarg = 'book_id'
    success_message = 'Данные книги успешно изменены'

    def post(self, request, *args, **kwargs):
        self.success_url = reverse('p_library:books_list', kwargs={
            'author_id': Book.objects.get(pk=self.kwargs['book_id']).author.id})
        return super().post(self, request, *args, **kwargs)


class BookDeleteView(SuccessMessageMixin, DeleteView, BookEditView, BookEditMixin, BookMixin):
    template_name = 'book_delete.html'
    model = Book
    fields = '__all__'
    pk_url_kwarg = 'book_id'
    success_message = 'Книга удалена'

    def post(self, request, *args, **kwargs):
        self.success_url = reverse('p_library:books_list', kwargs={
            'author_id': Book.objects.get(pk=self.kwargs['book_id']).author.id})
        messages.add_message(request, messages.SUCCESS, "Книга успешно удалена")
        
        return super().post(self, request, *args, **kwargs)
