from django.contrib import admin
from django.urls import include, path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('signin/', views.SignIn.as_view(), name='sign-in'),
    path('accounts/signup', views.signup, name='sign-up'),
    path('library/', views.library, name='library'),
    path('library/<int:book_id>', views.book_detail),
    path('library/add/', views.CreateBook.as_view(), name='create-book'),
    path('library/<int:pk>/delete/', views.DeleteBook.as_view(), name='delete-book'),
    path('booklists/', views.booklists, name='booklists'),
    path('booklists/<int:booklist_id>', views.booklist_detail, name='booklist-detail'),
    path('booklists/create', views.CreateBookList.as_view(), name='create-booklist'),
    path('booklists/<int:pk>/update', views.UpdateBookList.as_view(), name='update-booklist'),
    path('booklists/<int:booklist_id>/remove-book/<int:book_id>', views.remove_book, name='remove-book'),
    path('booklists/<int:pk>/delete', views.DeleteBookList.as_view(), name='delete-booklist'),
]