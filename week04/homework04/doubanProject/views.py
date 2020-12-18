from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie as mv
# Create your views here.

# def douban_firstpage(request):
#     return HttpResponse("Hello, world. This is first page for homework Douban.")

def index_page(request):
    n = mv.objects.all().filter(start__gt=3)

    return render(request,'index.html',locals())