from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
import pandas as pd
from .models import UploadHistory
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io

@api_view(['POST'])
def upload_csv(request):
    file = request.FILES.get('file')
    df = pd.read_csv(file)

    total_count = len(df)
    avg_flowrate = df['Flowrate'].mean()
    avg_pressure = df['Pressure'].mean()
    avg_temperature = df['Temperature'].mean()
    type_distribution = df['Type'].value_counts().to_dict()

    # Save to DB
    UploadHistory.objects.create(
        total_count=total_count,
        avg_flowrate=avg_flowrate,
        avg_pressure=avg_pressure,
        avg_temperature=avg_temperature
    )

    # Keep only last 5 records
    qs = UploadHistory.objects.order_by('-uploaded_at')
    if qs.count() > 5:
        for obj in qs[5:]:
            obj.delete()

    return Response({
        "total_count": total_count,
        "avg_flowrate": avg_flowrate,
        "avg_pressure": avg_pressure,
        "avg_temperature": avg_temperature,
        "type_distribution": type_distribution
    })


@api_view(['GET'])
def history(request):
    data = UploadHistory.objects.order_by('-uploaded_at').values(
        'uploaded_at', 'total_count', 'avg_flowrate', 'avg_pressure', 'avg_temperature'
    )
    return Response(list(data))


@api_view(['GET'])
def generate_pdf(request):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    text = p.beginText(40, 800)

    text.textLine("FOSSEE CSV Analyzer - Report")
    text.textLine("------------------------------")

    last = UploadHistory.objects.last()

    if last:
        text.textLine(f"Total Count: {last.total_count}")
        text.textLine(f"Average Flowrate: {last.avg_flowrate}")
        text.textLine(f"Average Pressure: {last.avg_pressure}")
        text.textLine(f"Average Temperature: {last.avg_temperature}")
    else:
        text.textLine("No data available.")

    p.drawText(text)
    p.showPage()
    p.save()

    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')
