# Url диспетчер приложения p_library
from django.urls import path
from p_library.views import (
    BookListView, BookDetailView, BookCreateView, BookUpdateView, BookDeleteView, 
    author_create
)

app_name = 'p_library'

urlpatterns = [
    path('<int:author_id>', BookListView.as_view(), name='books_list'),
    path('book/<int:book_id>', BookDetailView.as_view(), name='book_detail'),
    path('book/<int:author_id>/add', BookCreateView.as_view(), name='book_add'),
    path('book/<int:book_id>/update', BookUpdateView.as_view(), name='book_update'),
    path('book/<int:book_id>/delete',BookDeleteView.as_view(), name='book_delete'),
    path('author/add', author_create, name='author_add')

]
