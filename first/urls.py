
from django.contrib import admin
from django.urls import path

from django.contrib.auth.views import LoginView
import proj.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', proj.views.main_menu,name='main_menu'),
    path('main', proj.views.maintwo_menu,name='maintwo_menu'),
    path('submit-error/', proj.views.submit_error, name='submit_error'),
    path("register/", proj.views.register_page, name="register"),
    path(
        "login/",
        LoginView.as_view(
            template_name="auth/login.html", next_page=proj.views.profile_page
        ),
        name="login",
    ),
    path("logout/", proj.views.logout_view, name="logout"),
]