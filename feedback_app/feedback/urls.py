from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('generate_qr/', views.generate_qr_code, name='generate_qr'),
    path('form/', views.submit_form, name='submit_form'),
    path('update_questions/', views.update_questions, name='update_questions'),
    path('download_pdf/<int:response_id>/', views.download_pdf, name='download_pdf'),
    path('thank_you/', views.thank_you, name='thank_you'),  # Added URL for thank you page
    path('view_response/<int:response_id>/', views.view_response, name='view_response'),  # View response URL
    path('delete_response/<int:response_id>/', views.delete_response, name='delete_response'),  # Delete response URL
]
