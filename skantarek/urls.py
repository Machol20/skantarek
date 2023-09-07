"""
URL configuration for skantarek project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""



from django.contrib import admin
from django.urls import path
from wyszukiwarka_ulic import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.StreetSearchView.as_view(), name='search_streets'),
    path('secure_view/', views.SecureView.as_view(), name='secure_view'),
    path('street_services/', views.StreetServicesView.as_view(), name='street_services'),
    path('salesmen/', views.SalesmenSalesView.as_view(), name='salesmen_sales'),
    path('offers/', views.StreetOffersView.as_view(), name='offers_streets'),
    path('import_excel/', views.ImportExcelView.as_view(), name='import_excel'),
]

