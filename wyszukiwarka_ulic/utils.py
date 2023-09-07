from .models import Salesman, Sell, ForSale, Building, Street, Offer, StreetOffer
import pandas as pd


def import_data_from_excel(file):
    """
    Import data from excel file.
    """

    df = pd.read_excel(file)

    buildings = []
    streets = []
    sells = {}
    for_sales = {}
    salesmen = {}
    offers = {}
    street_offers = []

    for index, row in df.iterrows():
        last_name, first_name = row['RKS'].split(' ')
        salesman_id = f'{last_name}{first_name}'
        salesman = Salesman(
            imie=first_name,
            nazwisko=last_name,
            id=salesman_id
        )
        salesmen[salesman_id] = salesman

        sell = Sell(
            nazwa=row['SELL_NAME'],
            telewizja_internet=row['TELEWIZJA_INTERNET'],
            internet=row['INTERNET'],
            telefon=row['TELEFON'],
            internet_premium=row['INTERNET_PREMIUM'],
            BI=row['BI'],
            sprzedawca=salesmen[salesman_id]
        )
        sells[row['SELL_ID']] = sell

        for_sale = ForSale(
            nazwa=row['FOR_SALE_NAME'],
            telewizja_internet=row['FOR_SALE_TELEWIZJA_INTERNET'],
            internet=row['FOR_SALE_INTERNET'],
            telefon=row['FOR_SALE_TELEFON'],
            internet_premium=row['FOR_SALE_INTERNET_PREMIUM'],
            BI=row['FOR_SALE_BI']
        )
        for_sales[row['FOR_SALE_ID']] = for_sale

        building = Building(
            building_id=row['BUILDING_ID'],
            wojewodztwo=row['WOJEWODZTWO'],
            comunity=row['COMUNITY'],
            city_name=row['CITY_NAME'],
            street_name=row['STREET_NAME'],
            building_number=row['BUILDING_NUMBER'],
            building_post_code=row['BUILDING_POST_CODE'],
            hp=row['HP'],
            net_nmbr=row['NET_NMBR'],
            penetracja=row['PENETRACJA'],
            bitrate=row['BITRATE'],
            zakres_predkosci=row['Zakres Prędkości'],
            czarna_lista=row['CZARNA_LISTA'],
            naj_technologia=row['NAJ_TECHNOLOGIA']
        )
        buildings.append(building)

        street = Street(
            ulica=row['STREET_NAME'],
            numer_bloku=row['BUILDING_NUMBER'],
            numer_mieszkania=row.get('NUMER_MIESZKANIA', ''),
            kod_pocztowy=row['BUILDING_POST_CODE'],
            sell=sells.get(row['SELL_ID']),
            for_sale=for_sales.get(row['FOR_SALE_ID'])
        )
        streets.append(street)

        if isinstance(row['ADNOTACJE'], str):
            offers_titles = [title for title in row['ADNOTACJE'].split(',') if title]
            for offer_title in offers_titles:
                offer = Offer(
                    title=offer_title
                )
                offers[offer_title] = offer

                street_offer_relation = StreetOffer(
                    street=street,
                    offer=offer
                )
                street_offers.append(street_offer_relation)

    Salesman.objects.bulk_create(salesmen.values())
    Offer.objects.bulk_create(offers.values())
    Sell.objects.bulk_create(sells.values())
    ForSale.objects.bulk_create(for_sales.values())
    Building.objects.bulk_create(buildings)
    Street.objects.bulk_create(streets)
    StreetOffer.objects.bulk_create(street_offers)