from django.shortcuts import render

from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render

from FridgeApp.models import *


# Create your views here.


def view_main(request):
    produkty = Produkt.objects.all()
    przepisy = Przepis.objects.all()
    return render(request, 'index.html', {"produkty": produkty, "przepisy":przepisy})
