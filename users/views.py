from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from users.forms import CustomUserCreationForm, LoginForm
from django.contrib import messages


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            request.session['email'] = form.cleaned_data.get('email')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration_form.html', {'form': form})


def user_login(request):
    email = request.session.pop('email', '')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                if user.is_user:
                    return redirect('books:library')
                elif user.is_staff:
                    return redirect('books:staff')
            else:
                messages.error(request, 'Invalid email or password')
    else:
        form = LoginForm(initial={'email': email})

    return render(request, 'login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))
