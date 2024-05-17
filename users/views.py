from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from users.forms import CustomUserCreationForm, LoginForm


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
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
                if user.is_user:
                    login(request, user)
                    return redirect('library')
                elif user.is_staff:
                    login(request, user)
                    return redirect('staff')
                else:
                    form.add_error('email', 'Invalid email or password')
    else:
        form = LoginForm(initial={'email': email})
    return render(request, 'login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))
