# surveillance_do/models.py
from django.db import models

class StationSurveillanceDO(models.Model):
    nom = models.CharField(max_length=100)
    localisation = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.nom}"

class MesureSurveillanceDO(models.Model):
    station = models.ForeignKey(StationSurveillanceDO, on_delete=models.CASCADE)
    date_mesure = models.DateField()

    # Données de hauteur d'eau
    valeur_reglet_1 = models.FloatField(help_text="Valeur lue sur le réglet de contrôle 1")
    valeur_mesuree_1 = models.FloatField(help_text="Valeur mesurée sur site 1")
    ecart_1 = models.FloatField(help_text="Écart 1", blank=True, null=True)

    valeur_reglet_2 = models.FloatField(help_text="Valeur lue sur le réglet de contrôle 2")
    valeur_mesuree_2 = models.FloatField(help_text="Valeur mesurée sur site 2")
    ecart_2 = models.FloatField(help_text="Écart 2", blank=True, null=True)

    valeur_reglet_3 = models.FloatField(help_text="Valeur lue sur le réglet de contrôle 3")
    valeur_mesuree_3 = models.FloatField(help_text="Valeur mesurée sur site 3")
    ecart_3 = models.FloatField(help_text="Écart 3", blank=True, null=True)

    valeur_reglet_4 = models.FloatField(help_text="Valeur lue sur le réglet de contrôle 4")
    valeur_mesuree_4 = models.FloatField(help_text="Valeur mesurée sur site 4")
    ecart_4 = models.FloatField(help_text="Écart 4", blank=True, null=True)

    # Données de débit
    valeur_loi_hydraulique_1 = models.FloatField(help_text="Valeur donnée par la loi hydraulique 1")
    valeur_mesuree_debit_1 = models.FloatField(help_text="Valeur mesurée de débit 1")
    erreur_1 = models.FloatField(help_text="Erreur 1", blank=True, null=True)

    valeur_loi_hydraulique_2 = models.FloatField(help_text="Valeur donnée par la loi hydraulique 2")
    valeur_mesuree_debit_2 = models.FloatField(help_text="Valeur mesurée de débit 2")
    erreur_2 = models.FloatField(help_text="Erreur 2", blank=True, null=True)

    valeur_loi_hydraulique_3 = models.FloatField(help_text="Valeur donnée par la loi hydraulique 3")
    valeur_mesuree_debit_3 = models.FloatField(help_text="Valeur mesurée de débit 3")
    erreur_3 = models.FloatField(help_text="Erreur 3", blank=True, null=True)

    valeur_loi_hydraulique_4 = models.FloatField(help_text="Valeur donnée par la loi hydraulique 4")
    valeur_mesuree_debit_4 = models.FloatField(help_text="Valeur mesurée de débit 4")
    erreur_4 = models.FloatField(help_text="Erreur 4", blank=True, null=True)

    class Meta:
        unique_together = ('station', 'date_mesure')

    def __str__(self):
        return f"{self.station.nom} - {self.date_mesure}"

    def save(self, *args, **kwargs):
        # Calculer les écarts
        self.ecart_1 = self.valeur_mesuree_1 - self.valeur_reglet_1
        self.ecart_2 = self.valeur_mesuree_2 - self.valeur_reglet_2
        self.ecart_3 = self.valeur_mesuree_3 - self.valeur_reglet_3
        self.ecart_4 = self.valeur_mesuree_4 - self.valeur_reglet_4

        # Calculer les erreurs et les formater
        self.erreur_1 = round((self.valeur_mesuree_debit_1 - self.valeur_loi_hydraulique_1) / self.valeur_loi_hydraulique_1 * 100, 2)
        self.erreur_2 = round((self.valeur_mesuree_debit_2 - self.valeur_loi_hydraulique_2) / self.valeur_loi_hydraulique_2 * 100, 2)
        self.erreur_3 = round((self.valeur_mesuree_debit_3 - self.valeur_loi_hydraulique_3) / self.valeur_loi_hydraulique_3 * 100, 2)
        self.erreur_4 = round((self.valeur_mesuree_debit_4 - self.valeur_loi_hydraulique_4) / self.valeur_loi_hydraulique_4 * 100, 2)

        super().save(*args, **kwargs)
