from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Receiver
# Create your views here.


def index(request):
    """Página inicial """
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('gnss_iot:profile', args=[request.user.id]))
    else:
        return render(request, 'gnss_iot/index.html')

def profile(request, user_id):
    dados = Receiver.objects.filter(owner=request.user)
    
    context={
        'dados':dados,
    }
    return render(request, 'gnss_iot/profile.html', context=context)