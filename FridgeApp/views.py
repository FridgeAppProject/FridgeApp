from django.shortcuts import render, redirect

from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate

from FridgeApp.models import *





def view_main(request):
    value = request.COOKIES.get('auth')
    if value is None:
        return HttpResponseRedirect("login")
    u = value.split(" ")

    if Uzytkownik.objects.filter(login=u[0], haslo=u[1]).count() == 0:
        HttpResponseRedirect("login")
    else:
        user = Uzytkownik.objects.get(login=u[0], haslo=u[1])
    produkty_uzytkownika = Produkty_uzytkownika.objects.filter(id_uzytkownika=user.id)
    id_prod = []
    for p in produkty_uzytkownika:
        id_prod.append(int(p.id_produktu))
    produkty = Produkt.objects.all().order_by('nazwa')

    szukany_skladnik = request.POST.get("Składnik")
    if szukany_skladnik != None:
        produkty_filtr = produkty.filter(nazwa__contains=szukany_skladnik)
    else:
        produkty_filtr = produkty
    przepisy = Przepis.objects.all()
                                        #DODAWANIE PRODUKTU#
    if request.POST.get('addProdukt') is not None and request.POST.get('addIlosc') is not None:
        if int(request.POST.get('addProdukt')) in id_prod:
            addProdukt = Produkty_uzytkownika.objects.get(id_produktu=request.POST.get('addProdukt'))
            addProdukt.addProdukt(request.POST.get('addIlosc'))
            addProdukt.save()
            return redirect('/')
        else:
            addProdukt = Produkty_uzytkownika(id_uzytkownika=user.id, id_produktu=request.POST.get('addProdukt'),
                                              ilosc=request.POST.get('addIlosc'))
            addProdukt.save()
            return redirect('/')

    return render(request, 'index.html', {"produkty_filtr": produkty_filtr, "id_prod": id_prod, "przepisy": przepisy, "produkty_uzytkownika": produkty_uzytkownika, "produkty": produkty})
                                        #END DODAWANIE PRODUKTU END#


def view_login(request):
    login = request.POST.get('login')
    haslo = request.POST.get('haslo')

    if Uzytkownik.objects.filter(login=login, haslo=haslo).count() != 0:
        response = HttpResponse("<script>window.location.replace('http://localhost:8000/')</script>")
        response.set_cookie('auth', login+" "+haslo)

        return response
    else:
        return render(request, 'login.html', {})
