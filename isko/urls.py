from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('applicant/', views.applicant, name='applicant'),
    path('honors/', views.honors, name='honors'),
    path('sibling/', views.sibling, name='sibling'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('query/', views.query, name='query'),
    path('manage/', views.manage, name='manage'),
    path('programs/', views.programs, name='programs'),
    path('about/', views.about, name='about'),

    path('users/', views.user_list, name='user_list'),
    path('users/<int:pk>/', views.user_detail, name='user_detail'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:pk>/update/', views.user_update, name='user_update'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),
    
    path('applicantdetails/', views.applicantdetails_list, name='applicantdetails_list'),
    path('applicantdetails/<int:pk>/', views.applicantdetails_detail, name='applicantdetails_detail'),
    path('applicantdetails/create/', views.applicantdetails_create, name='applicantdetails_create'),
    path('applicantdetails/<int:pk>/update/', views.applicantdetails_update, name='applicantdetails_update'),
    path('applicantdetails/<int:pk>/delete/', views.applicantdetails_delete, name='applicantdetails_delete'),
    
    path('honors/', views.honors_list, name='honors_list'),
    path('honors/<int:pk>/', views.honors_detail, name='honors_detail'),
    path('honors/create/', views.honors_create, name='honors_create'),
    path('honors/<int:pk>/update/', views.honors_update, name='honors_update'),
    path('honors/<int:pk>/delete/', views.honors_delete, name='honors_delete'),
    
    path('siblings/', views.sibling_list, name='sibling_list'),
    path('siblings/<int:pk>/', views.sibling_detail, name='sibling_detail'),
    path('siblings/create/', views.sibling_create, name='sibling_create'),
    path('siblings/<int:pk>/update/', views.sibling_update, name='sibling_update'),
    path('siblings/<int:pk>/delete/', views.sibling_delete, name='sibling_delete'),
]