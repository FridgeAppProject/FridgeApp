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
            addProdukt = Produkty_uzytkownika.objects.get(id_produktu=request.POST.get('addProdukt'), id_uzytkownika=user.id)
            addProdukt.addProdukt(request.POST.get('addIlosc'))
            addProdukt.save()
            return redirect('/')
        else:
            addProdukt = Produkty_uzytkownika(id_uzytkownika=user.id, id_produktu=request.POST.get('addProdukt'),
                                              ilosc=request.POST.get('addIlosc'))
            addProdukt.save()
            return redirect('/')
                                      # END DODAWANIE PRODUKTU END#

    nazwa_przepisu = str(request.POST.get('nazwa_przepisu')).upper()
    kategoria = request.POST.get('kategoria')
    opis = request.POST.get('opis')
    produkty_przepisu = request.POST.get('produkty_przepisu')
    if nazwa_przepisu is not None and opis is not None and produkty_przepisu is not None:
        produkty_przepisu = produkty_przepisu.split(';')
        przepis = Przepis(nazwa=nazwa_przepisu,kategoria=kategoria, opis=opis)
        przepis.save()
        id_prze = Przepis.objects.get(nazwa=nazwa_przepisu).id
        for x in produkty_przepisu:
            dane = x.split('_')
            if len(dane) == 2:
                pro_prze = Produkty_przepisu(id_produktu=dane[0], id_przepisu=id_prze, ilosc=dane[1])
                pro_prze.save()
        return redirect('/')
    
    
    if request.POST.get('editIlosc') is not None and request.POST.get('editId') is not None:
        editp = Produkty_uzytkownika.objects.get(id=request.POST.get('editId'))
        editp.ilosc=request.POST.get('editIlosc')
        editp.save()
        return redirect('/')

    if request.POST.get('deleteId') is not None:
        deletep = Produkty_uzytkownika.objects.get(id=request.POST.get('deleteId'))
        deletep.delete()
        return redirect('/')
    #dostepne przepisy#

    dostepne_przepisy = []
    for przepis in przepisy:
        ok = True
        for p in Produkty_przepisu.objects.filter(id_przepisu=przepis.id):
            if produkty_uzytkownika.filter(id_produktu=p.id_produktu).count() > 0:
                produkty_uzytkownika.filter(id_produktu=p.id_produktu)
                spri = produkty_uzytkownika.get(id_produktu=p.id_produktu).ilosc
                if p.ilosc > spri:
                    ok = False
            else:
                ok = False
        if ok:
            dostepne_przepisy.append(przepis)
    if request.POST.get('co_wyswietlic') == "dostepne":
        przepisy = dostepne_przepisy
    if request.POST.get('co_wyswietlic') == "wszystko":
        przepisy = Przepis.objects.all()
    if request.POST.get('co_wyswietlic') is None:
        przepisy = dostepne_przepisy

    szukany_przepis = request.POST.get('Przepis')
    if szukany_przepis != None:
        przepisy = Przepis.objects.filter(nazwa__contains=szukany_przepis.upper())



    return render(request, 'index.html', {"user": user, "produkty_filtr": produkty_filtr, "id_prod": id_prod, "przepisy": przepisy, "produkty_uzytkownika": produkty_uzytkownika, "produkty": produkty,"produkty_przepisu": Produkty_przepisu.objects.all()})                                   


def view_login(request):
    login = request.POST.get('login')
    haslo = request.POST.get('haslo')

    if Uzytkownik.objects.filter(login=login, haslo=haslo).count() != 0:
        response = HttpResponse("<script>window.location.replace('http://fridge-application.herokuapp.com/')</script>")
        response.set_cookie('auth', login+" "+haslo)

        return response
    else:
        return render(request, 'login.html', {})
