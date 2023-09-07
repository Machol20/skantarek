import pytest
from django.urls import reverse
from .forms import StreetSearchForm, StreetServicesForm, SalesmenForm, OffersForm, ImportExcelForm
from .models import Street, Sell, Salesman, Offer


# /
@pytest.mark.django_db
def test_search_streets_view_get(client):
    response = client.get(reverse('search_streets'))
    assert response.status_code == 200
    assert 'form' in response.context
    assert isinstance(response.context['form'], StreetSearchForm)


@pytest.mark.django_db
def test_search_streets_view_empty_search_results(client):
    response = client.post(reverse('search_streets'), data={'search_query': 'ulica'})
    assert response.status_code == 200
    assert response.context['queryset'].count() == 0


@pytest.mark.django_db
def test_search_streets_view_not_empty_search_results(client):
    Street.objects.create(ulica='Ulica', numer_bloku='1', kod_pocztowy='00-000')
    response = client.post(reverse('search_streets'), data={'search_query': 'ulica'})
    assert response.status_code == 200
    assert response.context['queryset'].count() == 1


# /secure_view
@pytest.mark.django_db
def test_secure_view_unauthorized(client):
    response = client.get(reverse('secure_view'))
    assert response.status_code == 302
    assert '/login/' in response.url


@pytest.mark.django_db
def test_secure_view_authorized(admin_client):
    response = admin_client.get(reverse('secure_view'))
    assert response.status_code == 200


# /street_services
@pytest.mark.django_db
def test_street_services_view_get(client):
    response = client.get(reverse('street_services'))
    assert response.status_code == 200
    assert 'form' in response.context
    assert isinstance(response.context['form'], StreetServicesForm)


@pytest.mark.django_db
def test_street_services_view_empty_search_results(client):
    response = client.post(reverse('street_services'), data={'has_internet': True, 'has_television': True,
                                                             'has_phone': True})
    assert response.status_code == 200
    assert response.context['queryset'].count() == 0


@pytest.mark.django_db
def test_street_services_not_empty_search_results(client):
    sell = Sell.objects.create(nazwa='Sell', telewizja_internet=True, internet=True, telefon=True, internet_premium=True)
    Street.objects.create(ulica='Ulica', numer_bloku='1', kod_pocztowy='00-000', sell=sell)
    response = client.post(reverse('street_services'), data={'has_internet': True, 'has_television': True,
                                                             'has_phone': True})
    assert response.status_code == 200
    assert response.context['queryset'].count() == 1


# /salesmen
@pytest.mark.django_db
def test_salesmen_view_get(client):
    response = client.get(reverse('salesmen_sales'))
    assert response.status_code == 200
    assert 'form' in response.context
    assert isinstance(response.context['form'], SalesmenForm)


@pytest.mark.django_db
def test_salesmen_view_invalid_form(client):
    response = client.post(reverse('salesmen_sales'))
    assert response.status_code == 200
    assert response.context['form'].is_valid() is False
    assert len(response.context['form'].fields['salesman'].choices) == 1


@pytest.mark.django_db
def test_salesmen_not_empty_search_results(client):
    salesman = Salesman.objects.create(id='FirstNameLastName', imie='FirstName', nazwisko='LastName')
    Sell.objects.create(nazwa='Sell', telewizja_internet=True, internet=True, telefon=True, internet_premium=True,
                        sprzedawca=salesman)
    response = client.post(reverse('salesmen_sales'), data={'salesman': salesman.id})
    assert response.status_code == 200
    assert response.context['queryset'].count() == 1


# /offers
@pytest.mark.django_db
def test_offers_view_get(client):
    response = client.get(reverse('offers_streets'))
    assert response.status_code == 200
    assert 'form' in response.context
    assert isinstance(response.context['form'], OffersForm)


@pytest.mark.django_db
def test_offers_view_invalid_form(client):
    response = client.post(reverse('offers_streets'))
    assert response.status_code == 200
    assert response.context['form'].is_valid() is False
    assert len(response.context['form'].fields['offers'].choices) == 0


@pytest.mark.django_db
def test_offers_not_empty_search_results(client):
    offer = Offer.objects.create(title='Offer')
    street = Street.objects.create(ulica='Ulica', numer_bloku='1', kod_pocztowy='00-000')
    street.offers.set([offer])
    response = client.post(reverse('offers_streets'), data={'offers': [offer.title]})
    assert response.status_code == 200
    assert response.context['queryset'].count() == 1


# /import_excel
@pytest.mark.django_db
def test_import_excel_view_get(client):
    response = client.get(reverse('import_excel'))
    assert response.status_code == 200
    assert 'form' in response.context
    assert isinstance(response.context['form'], ImportExcelForm)


@pytest.mark.django_db
def test_import_excel_view_invalid_form(client):
    response = client.post(reverse('import_excel'))
    assert response.status_code == 200
    assert 'form' in response.context
    assert isinstance(response.context['form'], ImportExcelForm)
    assert response.context['form'].is_valid() is False
