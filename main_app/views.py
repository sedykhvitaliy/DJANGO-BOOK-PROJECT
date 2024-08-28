from django import views
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import BookList, Book
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


def home(request):
    latest_books = Book.objects.order_by('-id')[:5]  
    return render(request, 'home.html', {'latest_books': latest_books})


class SignIn(LoginView):
    template_name = 'signin.html'


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('booklists')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    return render(request, 'signup.html', {
        'form': form,
        'error_message': error_message
    })


@login_required
def booklists(request):
    booklists = BookList.objects.filter(user=request.user)
    return render(request, 'booklists.html', {'booklists': booklists})\



@login_required
def booklist_detail(request, booklist_id):
    booklist = BookList.objects.get(id=booklist_id)
    books = booklist.books.all()
    return render(request, 'booklist_detail.html', {
        'booklist': booklist,
        'books': books,
    })


@login_required
def library(request):
    books = Book.objects.filter(user=request.user)
    return render(request, 'library.html', {'books': books})


@login_required
def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    return render(request, 'book_detail.html', {'book': book})


class CreateBook(LoginRequiredMixin, CreateView):
    model = Book
    fields = ['title', 'author']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DeleteBook(LoginRequiredMixin, DeleteView):
    model = Book
    success_url = '/library/'

class UpdateBook(LoginRequiredMixin, UpdateView):
    model = Book
    fields = ['title', 'author']
    template_name = 'book_edit.html'
    success_url = '/library/'

class CreateBookList(LoginRequiredMixin, CreateView):
    model = BookList
    fields = ['title']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    

class UpdateBookList(LoginRequiredMixin, UpdateView):
    model = BookList
    fields = ['title', 'books']
    
    def form_valid(self, form):
        form.instance.books.add(*form.cleaned_data['books'])
        return super().form_valid(form)


@login_required
def remove_book(request, booklist_id, book_id):
    booklist = BookList.objects.get(id=booklist_id)
    booklist.books.remove(book_id)
    return redirect('booklist-detail', booklist_id=booklist.id)
    

class DeleteBookList(LoginRequiredMixin, DeleteView):
    model = BookList
    success_url = '/booklists/'