from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import ContextMixin, TemplateView
from django.views.generic.edit import ProcessFormView
from django.views.generic.edit import (
    CreateView, UpdateView, DeleteView,
)
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from p_library.models import Author, Book, Friend
from p_library.forms import AuthorForm, BookForm, FriendForm

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
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
        try:
            author_by = Author.objects.get(pk=self.kwargs['author_id'])  
        except ObjectDoesNotExist:
            author_by = Author.objects.first()
        
        self.author_by = author_by  
        return author_by

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.author_by == None:
            author_by = Author.objects.get(pk=self.kwargs['author_id'] or 1)
            context['author_by'] = author_by
        else:
            context['author_by'] = self.author_by
        return context


class BookMixin(ContextMixin):
    """Примесь, добавляющая в контекст автора, которому принадлежить книга"""

    author_by = None

    def get_author(self, **kwargs):
        try:
            author_by = Book.objects.get(pk=self.kwargs['book_id']).author
        except Book.DoesNotExist:
            raise Http404
        
        self.author_by = author_by
        return author_by

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.author_by == None:
            author_by = Book.objects.get(
                pk=self.kwargs['book_id']).author
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

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author_form'] = AuthorForm(instance=self.get_author())
        return context
    


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
        self.initial['friend'] = Friend.objects.first()
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

    def get(self, request, *args, **kwargs):
        self.initial['friend'] = Book.objects.get(pk=self.kwargs['book_id']).friend
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.success_url = reverse('p_library:books_list', kwargs={
            'author_id': self.get_author().id})
        return super().post(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['friend_form'] = FriendForm(instance=Book.objects.get(pk=self.kwargs['book_id']))
        return context
    

class BookDeleteView(SuccessMessageMixin, DeleteView, BookEditView, BookEditMixin, BookMixin):
    template_name = 'book_delete.html'
    model = Book
    fields = '__all__'
    pk_url_kwarg = 'book_id'
    success_message = 'Книга удалена'

    def post(self, request, *args, **kwargs):
        self.success_url = reverse('p_library:books_list', kwargs={
            'author_id': self.get_author().id})
        messages.add_message(request, messages.SUCCESS,"Книга успешно удалена")

        return super().post(request, *args, **kwargs)


class AuthorCreateView(TemplateView):
    form = None

    def post(self, request, *args, **kwargs):
        self.form = AuthorForm(request.POST)
        if self.form.is_valid():
            author = self.form.save()
            messages.add_message(request, messages.SUCCESS,f"Автор {author} успешно добавлен")
            return redirect('p_library:books_list', author_id = author.id)
        else:
            return redirect('p_library:books_list', author_id = Author.objects.first().id)


class AuthorUpdateView(TemplateView):
    form = None

    def post(self, request, *args, **kwargs):
        self.form = AuthorForm(request.POST)
        if self.form.is_valid():
            author = Author.objects.get(pk=self.kwargs['author_id'])
            author.full_name = self.form.cleaned_data['full_name']
            author.birth_year = self.form.cleaned_data['birth_year']
            author.country = self.form.cleaned_data['country']
            author = self.form.save()
            messages.add_message(request, messages.SUCCESS,f"Данные автора: {author} успешно изменены")
            return redirect('p_library:books_list', author_id = author.id)
        else:
            return redirect('p_library:books_list', author_id = Author.objects.first().id)


class AuthorDeleteView(DeleteView):
    model = Author
    form_class = AuthorForm
    pk_url_kwarg = 'author_id'
    success_url = reverse_lazy("p_library:books_list", kwargs={'author_id': Author.objects.first().id})
    


class FriendCreateView(CreateView, AuthorMixin):
    template_name = 'friend_add.html'
    model = Friend
    form_class = FriendForm

    def post(self, request, *args, **kwargs):
        self.success_url = reverse('p_library:book_add', kwargs={
            'author_id': self.get_author().id})
        return super().post(request, *args, **kwargs)

class FriendUpdateView(UpdateView):
    template_name = 'friend_edit.html'
    model = Friend
    form_class = FriendForm
    pk_url_kwarg = 'friend_id'

    def post(self, request, *args, **kwargs):
        self.success_url = reverse('p_library:books_list', kwargs={
            'author_id': 1})
        return super().post(request, *args, **kwargs)
    

class FriendDeleteView(DeleteView):
    template_name = 'friend_delete.html'
    model = Friend
    form_class = FriendForm
    pk_url_kwarg = 'friend_id'

    def post(self, request, *args, **kwargs):
        self.success_url = reverse('p_library:books_list', kwargs={
            'author_id': 1})
        return super().post(request, *args, **kwargs)