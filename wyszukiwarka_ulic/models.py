from django.db import models


class Building(models.Model):
    """
    Representation of a single building.
    """
    building_id = models.IntegerField(primary_key=True)
    wojewodztwo = models.CharField(max_length=100)
    comunity = models.CharField(max_length=100)
    city_name = models.CharField(max_length=100)
    street_name = models.CharField(max_length=100)
    building_number = models.CharField(max_length=10)
    building_post_code = models.CharField(max_length=10)
    hp = models.CharField(max_length=100)
    net_nmbr = models.CharField(max_length=100)
    penetracja = models.CharField(max_length=100)
    bitrate = models.CharField(max_length=100)
    zakres_predkosci = models.CharField(max_length=100)
    czarna_lista = models.CharField(max_length=100)
    naj_technologia = models.CharField(max_length=100)

    def __str__(self):
        return f"Building ID: {self.building_id}, City: {self.city_name}, Street: {self.street_name}"



class Street(models.Model):
    """
    Representation of a single building or a single flat if it is a block of flats.
    Each object can have at most one current sell configuration.
    """
    ulica = models.CharField(max_length=100)
    numer_bloku = models.CharField(max_length=10, default='')
    numer_mieszkania = models.CharField(max_length=10, default='')
    kod_pocztowy = models.CharField(max_length=10)
    sell = models.ForeignKey('Sell', on_delete=models.CASCADE, related_name='streets', null=True)
    for_sale = models.ForeignKey('ForSale', on_delete=models.CASCADE, related_name='streets', null=True)
    offers = models.ManyToManyField('Offer', related_name='streets', related_query_name='street', through='StreetOffer')

    def __str__(self):
        return self.ulica


class Sell(models.Model):
    """
    Representation of a currently sold offer.
    """
    nazwa = models.CharField(max_length=100)
    telewizja_internet = models.BooleanField(default=False)
    internet = models.BooleanField(default=False)
    telefon = models.BooleanField(default=False)
    internet_premium = models.BooleanField(default=False)
    BI = models.BooleanField(default=True)
    sprzedawca = models.ForeignKey('Salesman', on_delete=models.SET_NULL, related_name='sales', null=True)

    def __str__(self):
        return self.nazwa


class ForSale(models.Model):
    """
    Representation of an offer to sell in the future.
    """
    nazwa = models.CharField(max_length=100)
    telewizja_internet = models.BooleanField(default=False)
    internet = models.BooleanField(default=False)
    telefon = models.BooleanField(default=False)
    internet_premium = models.BooleanField(default=False)
    BI = models.BooleanField(default=True)

    def __str__(self):
        return self.nazwa


class Salesman(models.Model):
    """
    Representation of a salesman that is responsible for particular sell.
    Each sell object can have at most one salesman.
    """
    id = models.CharField(primary_key=True, max_length=200)
    imie = models.CharField(max_length=100)
    nazwisko = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.imie} {self.nazwisko}'


class Offer(models.Model):
    """
    Representation of an offer.
    Each client (street) can get multiple offers and each offer can be proposed to multiple clients (streets).
    """
    title = models.CharField(primary_key=True, max_length=150)

    def __str__(self):
        return self.title


class StreetOffer(models.Model):
    """
    Many-to-many relation between client (street) and offer.
    """
    street = models.ForeignKey('Street', on_delete=models.CASCADE, null=False)
    offer = models.ForeignKey('Offer', on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f'{self.street} - {self.offer}'
