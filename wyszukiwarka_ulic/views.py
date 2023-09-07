from django.shortcuts import render
from django.views.generic import View
from .forms import (
    StreetSearchForm,
    StreetServicesForm,
    SalesmenForm,
    OffersForm,
    ImportExcelForm,
)
from .models import Street, Building, Sell, ForSale, Salesman, Offer
from .utils import import_data_from_excel
from django.contrib.auth.mixins import LoginRequiredMixin


class StreetSearchView(View):
    """
    Search for streets by its name.
    """

    def get(self, request, *args, **kwargs):
        form = StreetSearchForm()
        return render(request, "search_street.html", {"form": form})

    def post(self, request):
        form = StreetSearchForm(request.POST)
        if form.is_valid():
            search_query = form.cleaned_data["search_query"]
            streets = Street.objects.filter(ulica__icontains=search_query)
            return render(request, "search_results.html", {"queryset": streets})


class SecureView(LoginRequiredMixin, View):
    """
    List all available streets with search feature.
    Only registered users allowed.
    """

    def get(self, request, *args, **kwargs):
        streets = Street.objects.all()
        return render(request, "secure_view.html", {"streets": streets})

    def post(self, request):
        query = request.POST.get("search_query", "")
        streets = Street.objects.filter(ulica__icontains=query)
        return render(request, "secure_view.html", {"streets": streets})


class SalesmenSalesView(View):
    """
    List all sales related to given salesman.
    """

    def get(self, request, *args, **kwargs):
        form = SalesmenForm()
        return render(request, "search_salesmen.html", {"form": form})

    def post(self, request):
        form = SalesmenForm(request.POST)
        if form.is_valid():
            salesman = form.cleaned_data["salesman"]
            sales = salesman.sales.all()
            return render(request, "search_results.html", {"queryset": sales})
        return render(request, "search_salesmen.html", {"form": form})


class StreetOffersView(View):
    """
    List all clients (streets) related to given offers.
    """

    def get(self, request, *args, **kwargs):
        form = OffersForm()
        return render(request, "search_offers.html", {"form": form})

    def post(self, request):
        form = OffersForm(request.POST)
        if form.is_valid():
            offers = form.cleaned_data["offers"]
            streets = Street.objects.filter(offers__in=offers).distinct()
            return render(request, "search_results.html", {"queryset": streets})
        return render(request, "search_offers.html", {"form": form})


class ImportExcelView(View):
    """
    Import data from excel file.
    """

    def get(self, request, *args, **kwargs):
        form = ImportExcelForm()

        return render(request, "import_excel.html", {"form": form})

    def post(self, request):
        form = ImportExcelForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"]
            truncate = form.cleaned_data["truncate"]
            if truncate:
                Salesman.objects.all().delete()
                Sell.objects.all().delete()
                ForSale.objects.all().delete()
                Building.objects.all().delete()
                Street.objects.all().delete()
                Offer.objects.all().delete()
            try:
                import_data_from_excel(file)
            except Exception as e:
                return render(
                    request,
                    "import_excel.html",
                    {"error_message": f"Wystąpił błąd: {e}"},
                )

            return render(
                request,
                "import_excel.html",
                {
                    "success_message": "Dane z pliku Excela zostały dodane do bazy danych."
                },
            )
        return render(request, "import_excel.html", {"form": form})


class StreetServicesView(View):
    """
    Search for streets by their features, like internet, phone, tv.
    """

    def get(self, request, *args, **kwargs):
        form = StreetServicesForm()

        return render(request, "street_services.html", {"form": form})

    def post(self, request):
        form = StreetServicesForm(request.POST)
        if form.is_valid():
            has_internet = form.cleaned_data["has_internet"]
            has_television = form.cleaned_data["has_television"]
            has_phone = form.cleaned_data["has_phone"]
            streets = Street.objects.filter(
                sell__internet=has_internet,
                sell__telewizja_internet=has_television,
                sell__telefon=has_phone,
            )
            return render(request, "search_results.html", {"queryset": streets})
