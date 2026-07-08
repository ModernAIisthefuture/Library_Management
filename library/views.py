from django.shortcuts import render, redirect, get_object_or_404

from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)

from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy

from .models import Book

from .forms import BookForm


from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):

    books = Book.objects.all()

    return render(
        request,
        'library/dashboard.html',
        {
            'books': books
        }
    )



class BookListView(LoginRequiredMixin, ListView):

    model = Book

    template_name = (
        'library/books/book_list.html'
    )

    context_object_name = 'books'



class BookCreateView(LoginRequiredMixin, CreateView):

    model = Book

    form_class = BookForm

    template_name = (
        'library/books/book_form.html'
    )

    success_url = reverse_lazy(
        'book_list'
    )



class BookUpdateView(LoginRequiredMixin, UpdateView):

    model = Book

    form_class = BookForm

    template_name = (
        'library/books/book_form.html'
    )

    success_url = reverse_lazy(
        'book_list'
    )



class BookDeleteView(LoginRequiredMixin, DeleteView):

    model = Book

    template_name = (
        'library/books/book_delete.html'
    )

    success_url = reverse_lazy(
        'book_list'
    )


@login_required
def borrow_book(request, pk):

    book = get_object_or_404(
        Book,
        id=pk
    )

    book.borrower = request.user

    book.available = False

    book.save()


    return redirect(
        'book_list'
    )


@login_required
def return_book(request, pk):

    book = get_object_or_404(
        Book,
        id=pk
    )

    book.borrower = None

    book.available = True

    book.save()


    return redirect(
        'book_list'
    )



def search_books(request):

    query = request.GET.get(
        'q'
    )

    books = Book.objects.filter(
        title__icontains=query
    )


    return render(
        request,
        'library/partials/search_results.html',
        {
            'books': books
        }
    )