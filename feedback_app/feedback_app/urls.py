from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', auth_views.LoginView.as_view(template_name='feedback/login.html'), name='login'),  # Ensure the correct template is used
    path('feedback/', include('feedback.urls')),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
