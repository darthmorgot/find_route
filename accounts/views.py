from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from accounts.forms import UserLoginForm, UserRegistrationForm


def login_view(request):
    form = UserLoginForm(request.POST or None)
    next_key = request.GET.get('next')

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        page = next_key or '/'

        return redirect(page)

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')


def registration_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return render(request, 'accounts/register_done.html', {'new_user': new_user})

        return render(request, 'accounts/register.html', {'form': form})

    else:
        form = UserRegistrationForm()
        return render(request, 'accounts/register.html', {'form': form})
