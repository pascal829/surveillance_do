# surveillance_do/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_stations_surveillance_do, name='liste_stations_surveillance_do'),
    path('<int:station_id>/', views.detail_station_surveillance_do, name='detail_station_surveillance_do'),
    path('<int:station_id>/ajouter_mesure/', views.ajouter_mesure_surveillance_do, name='ajouter_mesure_surveillance_do'),
    path('<int:station_id>/export_mesures/', views.export_mesures_surveillance_do, name='export_mesures_surveillance_do'),
    path('<int:station_id>/export_mesures_pdf/', views.export_mesures_surveillance_do_pdf, name='export_mesures_surveillance_do_pdf'),
]

