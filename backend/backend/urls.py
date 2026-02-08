from django.contrib import admin
from django.urls import path
from api.views import upload_csv, history, generate_pdf

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/upload/', upload_csv),
    path('api/history/', history),   # 👈 ADD THIS
    path('api/report/', generate_pdf),

]