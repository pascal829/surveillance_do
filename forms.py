# surveillance_do/forms.py
from django import forms
from .models import MesureSurveillanceDO

class MesureSurveillanceDOForm(forms.ModelForm):
    class Meta:
        model = MesureSurveillanceDO
        fields = ['date_mesure', 'valeur_reglet_1', 'valeur_mesuree_1', 'valeur_reglet_2', 'valeur_mesuree_2', 'valeur_reglet_3', 'valeur_mesuree_3', 'valeur_reglet_4', 'valeur_mesuree_4', 'valeur_loi_hydraulique_1', 'valeur_mesuree_debit_1', 'valeur_loi_hydraulique_2', 'valeur_mesuree_debit_2', 'valeur_loi_hydraulique_3', 'valeur_mesuree_debit_3', 'valeur_loi_hydraulique_4', 'valeur_mesuree_debit_4']
