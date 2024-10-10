from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('generate_qr/', views.generate_qr_code, name='generate_qr'),
    path('form/', views.submit_form, name='submit_form'),
    path('update_questions/', views.update_questions, name='update_questions'),
    path('download_pdf/<int:response_id>/', views.download_pdf, name='download_pdf'),
]
