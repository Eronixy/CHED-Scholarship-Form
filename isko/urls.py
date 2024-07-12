from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('applicant/', views.applicant, name='applicant'),
    path('honors/', views.honors, name='honors'),
    path('siblings/', views.siblings, name='siblings'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('query/', views.query, name='query'),
    path('manage/', views.manage, name='manage'),
    path('programs/', views.programs, name='programs'),
    path('about/', views.about, name='about'),

    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:pk>/update/', views.user_update, name='user_update'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),
    
    path('applicant_list/', views.applicant_list, name='applicant_list'),
    path('applicant/<int:pk>/update/', views.applicant_update, name='applicant_update'),
    path('applicant/<int:pk>/delete/', views.applicant_delete, name='applicant_delete'),
    
    path('honors_list/', views.honors_list, name='honors_list'),
    path('honors/create/', views.honors_create, name='honors_create'),
    path('honors/<int:pk>/update/', views.honors_update, name='honors_update'),
    path('honors/<int:pk>/delete/', views.honors_delete, name='honors_delete'),
    
    path('siblings_list/', views.siblings_list, name='siblings_list'),
    path('siblings/create/', views.siblings_create, name='siblings_create'),
    path('siblings/<int:pk>/update/', views.siblings_update, name='siblings_update'),
    path('siblings/<int:pk>/delete/', views.siblings_delete, name='siblings_delete'),
]