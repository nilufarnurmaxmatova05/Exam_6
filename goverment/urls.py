from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from goverment import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),

    # Autentifikatsiya
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout/', views.MyLogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('password-reset/', views.reset_password_request, name='password_reset_request'),
    path('password-reset/verify/', views.reset_password_verify, name='password_reset_verify'),

    # Parolni tiklash
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Vazirliklar
    path('ministers/', views.minister_list, name='minister_list'),
    path('ministers/<int:pk>/', views.minister_detail, name='minister_detail'),
    path('ministers/add/', views.minister_create, name='minister_create'),
    path('ministers/<int:pk>/edit/', views.minister_update, name='minister_update'),
    path('ministers/<int:pk>/delete/', views.minister_delete, name='minister_delete'),

    # Vazirlik
    path('ministries/', views.ministry_list, name='ministry_list'),
    path('ministries/<int:pk>/', views.ministry_detail, name='ministry_detail'),
    path('ministries/add/', views.ministry_create, name='ministry_create'),
    path('ministries/<int:pk>/edit/', views.ministry_update, name='ministry_update'),
    path('ministries/<int:pk>/delete/', views.ministry_delete, name='ministry_delete'),

    # Bo'limlar
    path('departments/', views.department_list, name='department_list'),
    path('departments/<int:pk>/', views.department_detail, name='department_detail'),
    path('departments/add/', views.department_create, name='department_create'),
    path('departments/<int:pk>/edit/', views.department_update, name='department_update'),
    path('departments/<int:pk>/delete/', views.department_delete, name='department_delete'),
]

# Media fayllarni ishlab turgan vaqtda ko'rsatish uchun
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)