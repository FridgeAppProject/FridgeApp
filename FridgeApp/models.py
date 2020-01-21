from django.db import models

# Create your models here.

class Produkt(models.Model):
    id = models.AutoField(primary_key=True)
    nazwa = models.CharField(max_length=256)
    jednostka = models.CharField(max_length=256)

    def __str__(self):
        return self.nazwa

class Przepis(models.Model):
    id = models.AutoField(primary_key=True)
    nazwa = models.CharField(max_length=256)
    kategoria = models.CharField(max_length=256)
    opis = models.CharField(max_length=8196)

    def __str__(self):
        return self.nazwa

class Produkty_przepisu(models.Model):
    id = models.AutoField(primary_key=True)
    id_przepisu = models.CharField(max_length=256)
    id_produktu = models.CharField(max_length=256)
    ilosc = models.CharField(max_length=256)

    def __str__(self):
        return self.id
class Produkty_uzytkownika(models.Model):
    id = models.AutoField(primary_key=True)
    id_uzytkownika = models.CharField(max_length=256)
    id_produktu = models.CharField(max_length=256)
    ilosc = models.CharField(max_length=256)

    def __str__(self):
        return self.id

class Uzytkownik(models.Model):
    id = models.AutoField(primary_key=True)
    login = models.CharField(max_length=256)
    haslo = models.CharField(max_length=256)

    def __str__(self):
        return self.login



