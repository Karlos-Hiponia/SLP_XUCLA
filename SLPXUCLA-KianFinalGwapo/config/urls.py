from django.contrib import admin
from django.urls import path, include
from XUCLA.views import register_view, login_view, logout_view, dashboard_view, home, password_reset_request_view, password_reset_code_view, password_reset_set_view
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", home, name="home"),
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path('', include('XUCLA.urls')),
    path('admin/', admin.site.urls),
    path('custom-password-reset/', password_reset_request_view, name='password_reset_request'),
    path('custom-password-reset/code/', password_reset_code_view, name='password_reset_code'),
    path('custom-password-reset/set/', password_reset_set_view, name='password_reset_set'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)