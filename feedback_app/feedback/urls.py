from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('generate_qr/', views.generate_qr_code, name='generate_qr'),
    path('form/', views.submit_form, name='submit_form'),
    path('update_questions/', views.update_questions, name='update_questions'),
    path('download_pdf/<int:response_id>/', views.download_pdf, name='download_pdf'),
    path('thank_you/', views.thank_you, name='thank_you'),
    path('view_response/<int:response_id>/', views.view_response, name='view_response'),
    path('delete_response/<int:response_id>/', views.delete_response, name='delete_response'),

    # Login and Logout URLs
    path('login/', LoginView.as_view(template_name='feedback/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),  # Use Django's built-in LogoutView
]
