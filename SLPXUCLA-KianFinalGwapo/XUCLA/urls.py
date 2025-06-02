from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path('submit-activity/', views.activity_form_view, name='submit-activity'),
    path('profile/', views.user_profile_view, name='user_profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('admin/users/', views.admin_user_list, name='admin_user_list'),
    path('admin/users/<int:user_id>/', views.admin_user_detail, name='admin_user_detail'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('superuser/manage-accounts/', views.superuser_manage_accounts, name='superuser_manage_accounts'),
    path('verify-email/', views.verify_email, name='verify_email'),
    path('resend-verification/', views.resend_verification, name='resend_verification'),
    path('custom-password-reset/', views.password_reset_request_view, name='password_reset_request'),
    path('custom-password-reset/code/', views.password_reset_code_view, name='password_reset_code'),
    path('custom-password-reset/set/', views.password_reset_set_view, name='password_reset_set'),
    path('admin/activity/<int:activity_id>/approve/', views.approve_activity, name='approve_activity'),
    path('admin/activity/<int:activity_id>/reject/', views.reject_activity, name='reject_activity'),

]