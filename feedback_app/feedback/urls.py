from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('generate_qr_code/', views.generate_qr_code, name='generate_qr_code'),
    path('form/', views.submit_form, name='submit_form'),
    path('update_questions/', views.update_questions, name='update_questions'),
    path('thank_you/', views.thank_you, name='thank_you'),
    path('view_response/<int:response_id>/', views.view_response, name='view_response'),
    path('delete_response/<int:response_id>/', views.delete_response, name='delete_response'),

    # Questions management
    path('questions/', views.question_list, name='question_list'),
    path('questions/edit/<int:question_id>/', views.edit_question, name='edit_question'),
    path('questions/delete/<int:question_id>/', views.delete_question, name='delete_question'),
    path('questions/add/', views.add_question, name='add_question'),

    # Login and Logout URLs
    path('login/', LoginView.as_view(template_name='feedback/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
