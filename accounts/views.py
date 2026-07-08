from django.shortcuts import render, redirect

from django.contrib.auth import (
    authenticate,
    login,
    logout
)

from django.contrib.auth.models import User

from .forms import RegisterForm


def index(request):
    return render(request, 'accounts/index.html')

def register_view(request):

    if request.method == "POST":

        form = RegisterForm(
            request.POST
        )

        if form.is_valid():

            user = form.save(
                commit=False
            )

            user.set_password(
                form.cleaned_data['password']
            )

            user.save()

            return redirect(
                'login'
            )


    else:

        form = RegisterForm()


    return render(
        request,
        'accounts/register.html',
        {
            'form': form
        }
    )





def login_view(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect('dashboard')

        return render(
            request,
            'accounts/login.html',
            {
                'error': 'Invalid username or password'
            }
        )

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('index')
