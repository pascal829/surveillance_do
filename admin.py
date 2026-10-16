# surveillance_do/admin.py
from django.contrib import admin
from .models import StationSurveillanceDO, MesureSurveillanceDO

@admin.register(StationSurveillanceDO)
class StationSurveillanceDOAdmin(admin.ModelAdmin):
    list_display = ('nom', 'localisation')
    list_filter = ('nom',)

@admin.register(MesureSurveillanceDO)
class MesureSurveillanceDOAdmin(admin.ModelAdmin):
    list_display = ('station', 'date_mesure', 'valeur_reglet_1', 'valeur_mesuree_1', 'ecart_1', 'valeur_reglet_2', 'valeur_mesuree_2', 'ecart_2', 'valeur_reglet_3', 'valeur_mesuree_3', 'ecart_3', 'valeur_reglet_4', 'valeur_mesuree_4', 'ecart_4', 'valeur_loi_hydraulique_1', 'valeur_mesuree_debit_1', 'erreur_1', 'valeur_loi_hydraulique_2', 'valeur_mesuree_debit_2', 'erreur_2', 'valeur_loi_hydraulique_3', 'valeur_mesuree_debit_3', 'erreur_3', 'valeur_loi_hydraulique_4', 'valeur_mesuree_debit_4', 'erreur_4')
    list_filter = ('station', 'date_mesure')
    date_hierarchy = 'date_mesure'

