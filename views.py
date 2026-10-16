# surveillance_do/views.py
from django.shortcuts import render, redirect
from .models import StationSurveillanceDO, MesureSurveillanceDO
from .forms import MesureSurveillanceDOForm
import matplotlib.pyplot as plt
import io
import base64
import csv
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

def liste_stations_surveillance_do(request):
    stations = StationSurveillanceDO.objects.all()
    return render(request, 'surveillance_do/liste.html', {'stations': stations})

def detail_station_surveillance_do(request, station_id):
    station = StationSurveillanceDO.objects.get(id=station_id)
    mesures = MesureSurveillanceDO.objects.filter(station=station).order_by('date_mesure')

    # Générer le graphique
    plt.figure(figsize=(10, 5))
    plt.plot([mesure.date_mesure for mesure in mesures], [mesure.valeur_mesuree_1 for mesure in mesures], marker='o', label='Valeur mesurée 1')
    plt.plot([mesure.date_mesure for mesure in mesures], [mesure.valeur_mesuree_2 for mesure in mesures], marker='o', label='Valeur mesurée 2')
    plt.plot([mesure.date_mesure for mesure in mesures], [mesure.valeur_mesuree_3 for mesure in mesures], marker='o', label='Valeur mesurée 3')
    plt.plot([mesure.date_mesure for mesure in mesures], [mesure.valeur_mesuree_4 for mesure in mesures], marker='o', label='Valeur mesurée 4')
    plt.xlabel('Date')
    plt.ylabel('Valeur')
    plt.title(f'Mesures pour {station.nom}')
    plt.legend()
    plt.grid(True)

    # Convertir le graphique en image base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png).decode('utf-8')
    buffer.close()

    return render(request, 'surveillance_do/detail.html', {'station': station, 'mesures': mesures, 'graph': graph})

def ajouter_mesure_surveillance_do(request, station_id):
    station = StationSurveillanceDO.objects.get(id=station_id)
    if request.method == 'POST':
        form = MesureSurveillanceDOForm(request.POST)
        if form.is_valid():
            mesure = form.save(commit=False)
            mesure.station = station
            mesure.save()
            return redirect('detail_station_surveillance_do', station_id=station.id)
    else:
        form = MesureSurveillanceDOForm()
    return render(request, 'surveillance_do/ajouter_mesure.html', {'form': form, 'station': station})

def export_mesures_surveillance_do(request, station_id):
    station = StationSurveillanceDO.objects.get(id=station_id)
    mesures = MesureSurveillanceDO.objects.filter(station=station).order_by('date_mesure')

    # Créer un fichier CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{station.nom}_mesures.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Valeur réglet 1', 'Valeur mesurée 1', 'Écart 1', 'Valeur réglet 2', 'Valeur mesurée 2', 'Écart 2', 'Valeur réglet 3', 'Valeur mesurée 3', 'Écart 3', 'Valeur réglet 4', 'Valeur mesurée 4', 'Écart 4', 'Valeur loi hydraulique 1', 'Valeur mesurée débit 1', 'Erreur 1', 'Valeur loi hydraulique 2', 'Valeur mesurée débit 2', 'Erreur 2', 'Valeur loi hydraulique 3', 'Valeur mesurée débit 3', 'Erreur 3', 'Valeur loi hydraulique 4', 'Valeur mesurée débit 4', 'Erreur 4'])

    for mesure in mesures:
        writer.writerow([mesure.date_mesure, mesure.valeur_reglet_1, mesure.valeur_mesuree_1, mesure.ecart_1, mesure.valeur_reglet_2, mesure.valeur_mesuree_2, mesure.ecart_2, mesure.valeur_reglet_3, mesure.valeur_mesuree_3, mesure.ecart_3, mesure.valeur_reglet_4, mesure.valeur_mesuree_4, mesure.ecart_4, mesure.valeur_loi_hydraulique_1, mesure.valeur_mesuree_debit_1, mesure.erreur_1, mesure.valeur_loi_hydraulique_2, mesure.valeur_mesuree_debit_2, mesure.erreur_2, mesure.valeur_loi_hydraulique_3, mesure.valeur_mesuree_debit_3, mesure.erreur_3, mesure.valeur_loi_hydraulique_4, mesure.valeur_mesuree_debit_4, mesure.erreur_4])

    return response

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import landscape
from reportlab.lib.pagesizes import A4


def export_mesures_surveillance_do_pdf(request, station_id):
    station = get_object_or_404(StationSurveillanceDO, id=station_id)
    mesures = MesureSurveillanceDO.objects.filter(station=station).order_by('date_mesure')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{station.nom}_mesures.pdf"'

    doc = SimpleDocTemplate(response, pagesize=landscape(A4))
    styles = getSampleStyleSheet()
    story = []

    title = Paragraph(f"Mesures pour {station.nom}", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 0.5 * inch))

    # Définition des entêtes et des données
    header_13_cols = ['Date', 'Valeur 1', 'Mesure 1', 'Écart 1', 'Valeur 2', 'Mesure 2', 'Écart 2', 'Valeur 3', 'Mesure 3', 'Écart 3', 'Valeur 4', 'Mesure 4', 'Écart 4']
    header_12_cols = ['Valeur loi 1', 'Valeur débit 1', 'Erreur 1 en %', 'Valeur loi 2', 'Valeur débit 2', 'Erreur 2 en %', 'Valeur loi 3', 'Valeur débit 3', 'Erreur 3 en %', 'Valeur loi 4', 'Valeur débit 4', 'Erreur 4 en %']

    data_13_cols = [header_13_cols]
    data_12_cols = [header_12_cols]

    for mesure in mesures:
        # Données pour le premier tableau (colonnes 1-13)
        row_13 = [
            str(mesure.date_mesure),
            str(mesure.valeur_reglet_1), str(mesure.valeur_mesuree_1), str(mesure.ecart_1),
            str(mesure.valeur_reglet_2), str(mesure.valeur_mesuree_2), str(mesure.ecart_2),
            str(mesure.valeur_reglet_3), str(mesure.valeur_mesuree_3), str(mesure.ecart_3),
            str(mesure.valeur_reglet_4), str(mesure.valeur_mesuree_4), str(mesure.ecart_4)
        ]
        data_13_cols.append(row_13)

        # Données pour le second tableau (colonnes 14-25)
        row_12 = [
            str(mesure.valeur_loi_hydraulique_1), str(mesure.valeur_mesuree_debit_1), str(mesure.erreur_1),
            str(mesure.valeur_loi_hydraulique_2), str(mesure.valeur_mesuree_debit_2), str(mesure.erreur_2),
            str(mesure.valeur_loi_hydraulique_3), str(mesure.valeur_mesuree_debit_3), str(mesure.erreur_3),
            str(mesure.valeur_loi_hydraulique_4), str(mesure.valeur_mesuree_debit_4), str(mesure.erreur_4)
        ]
        data_12_cols.append(row_12)

    # Création du premier tableau
    table1 = Table(data_13_cols, colWidths=[0.8*inch]*13) # Ajustez les largeurs des colonnes si besoin
    table1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), '#4287f5'),
        ('TEXTCOLOR', (0, 0), (-1, 0), '#ffffff'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 7),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), '#f8f8f8'),
        ('GRID', (0, 0), (-1, -1), 1, '#dddddd')
    ]))
    story.append(table1)
    story.append(Spacer(1, 0.2*inch)) # Espace entre les deux tableaux

    # Création du second tableau
    table2 = Table(data_12_cols, colWidths=[1.0*inch]*12) # Ajustez les largeurs des colonnes si besoin
    table2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), '#4287f5'),
        ('TEXTCOLOR', (0, 0), (-1, 0), '#ffffff'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 7),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), '#f8f8f8'),
        ('GRID', (0, 0), (-1, -1), 1, '#dddddd')
    ]))
    story.append(table2)

    doc.build(story)

    return response
