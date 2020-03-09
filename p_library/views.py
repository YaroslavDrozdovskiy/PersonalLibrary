from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
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
from p_library.forms import AuthorForm, BookForm


# Create your views here.

###################### Примеси и вспомогательные классы ###############################


class AuthorListMixin(ContextMixin):
    """Примесь,добавляющая в контекст список авторов"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authors'] = Author.objects.order_by('full_name')
        return context


class AuthorMixin(ContextMixin):
    """Примесь, добавляющая в контекст выбранного автора"""

    author_by = None

    def get_author(self, **kwargs):
        if self.author_by == None:
            author_by = Author.objects.get(pk=self.kwargs['author_id'] or 1)
            self.author_by = author_by
        else:
            author_by = self.author_by
        return author_by

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.author_by == None:
            author_by = Author.objects.get(
                pk=self.kwargs['author_id'] or 1)
            self.author_by = author_by
            context['author_by'] = author_by
        else:
            context['author_by'] = self.author_by
        return context


class BookMixin(ContextMixin):
    """Примесь, добавляющая в контекст автора, которому принадлежить книга"""

    author_by = None

    def get_author(self, **kwargs):
        if self.author_by == None:
            author_by = Book.objects.get(pk=self.kwargs['book_id'] or 1).author
            self.author_by = author_by
        else:
            author_by = self.author_by
        return author_by

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.author_by == None:
            author_by= Book.objects.get(
                pk=self.kwargs['book_id'] or 1).author
            context['author_by'] = author_by
        else:
            context['author_by'] = self.author_by
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
        return super().post(request, *args, **kwargs)


###################### Основные контроллеры ###############################

class BookListView(ListView, AuthorListMixin, AuthorMixin):
    """Контроллер списка книг"""

    template_name = 'books_list.html'
    paginate_by = 2

    def get_queryset(self):
        return Book.objects.filter(author=self.get_author()).order_by('title')


class BookDetailView(DetailView, BookEditMixin, BookMixin):
    template_name = 'book_detail.html'
    model = Book
    pk_url_kwarg = 'book_id'


class BookCreateView(SuccessMessageMixin, CreateView, BookEditMixin, AuthorMixin):
    template_name = 'book_add.html'
    model = Book
    form_class = BookForm
    success_message = 'Книга успешно добавлена'

    def get(self, request, *args, **kwargs):
        self.initial['author'] = self.get_author()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.success_url = reverse('p_library:books_list', kwargs={
            'author_id': self.get_author().id})
        return super().post(request, *args, **kwargs)


class BookUpdateView(SuccessMessageMixin, UpdateView, BookEditView, BookEditMixin, BookMixin):
    template_name = 'book_update.html'
    model = Book
    form_class = BookForm
    pk_url_kwarg = 'book_id'
    success_message = 'Данные книги успешно изменены'

    def post(self, request, *args, **kwargs):
        self.success_url = reverse('p_library:books_list', kwargs={
            'author_id': self.get_author().id})
        return super().post(request, *args, **kwargs)


class BookDeleteView(SuccessMessageMixin, DeleteView, BookEditView, BookEditMixin, BookMixin):
    template_name = 'book_delete.html'
    model = Book
    fields = '__all__'
    pk_url_kwarg = 'book_id'
    success_message = 'Книга удалена'

    def post(self, request, *args, **kwargs):
        self.success_url = reverse('p_library:books_list', kwargs={
            'author_id': self.get_author().id})
        messages.add_message(request, messages.SUCCESS,
                             "Книга успешно удалена")

        return super().post(request, *args, **kwargs)


class AuthorCreateView(SuccessMessageMixin, CreateView):
    model = Author
    form_class = AuthorForm
    success_url = reverse_lazy("p_library:books_list", kwargs={'author_id': 1})
    success_message = 'Добавлен автор'


class AuthorUpdateView(SuccessMessageMixin, UpdateView):
    template_name = 'includes/left-menu'
    model = Author
    form_class = AuthorForm
    pk_url_kwarg = 'author_id'
    success_url = reverse_lazy("p_library:books_list", kwargs={'author_id': 1})
    success_message = 'Данные автора изменены'


class AuthorDeleteView(SuccessMessageMixin, DeleteView):
    model = Author
    form_class = AuthorForm
    pk_url_kwarg = 'author_id'
    success_url = reverse_lazy("p_library:books_list", kwargs={'author_id': 1})
    success_message = 'Удалён автор'
