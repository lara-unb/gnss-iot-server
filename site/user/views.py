from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from .forms import RegisterForm

# Create your views here.


def login_view(request):
    if request.method == 'POST':
        authenticate_user = authenticate(username=request.POST['username'], password=request.POST['password'])
        login(request, authenticate_user)

        return redirect('gnss_iot:index')

    return render(request, 'user/login.html')


def logout_view(request):
    logout(request)
    return redirect('gnss_iot:index')


def register(request):
    if request.method != 'POST':
        form = RegisterForm()

    else:
        form = RegisterForm(data=request.POST)

        if form.is_valid():
            new_user = form.save_all()
            authenticate_user = authenticate(
                username=new_user.username, password=request.POST['password1'])
            login(request, authenticate_user)
            return redirect('gnss_iot:index')
    context = {'form': form}
    return render(request, 'user/register.html', context=context)
