from django.http import JsonResponse
from django.shortcuts import render
from episodes.models import Episode
from .models import Like


def index(request):
    obj = Episode.objects.all()[:3]
    ctx = {
        "obj": obj
    }
    return render(request, 'index.html', ctx)



