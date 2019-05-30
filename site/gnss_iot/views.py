from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

# Create your views here.


def index (request):
    """A página inicial do Gnss Iot"""
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('gnss_iot:profile', args=[request.user.id]))
    else:
        return render(request, 'gnss_iot/index.html')


def profile(request, user_id):
    dados = User.objects.filter(id = user_id)

    context = {'dados':dados}

    return render(request, 'gnss_iot/profile.html', context=context)