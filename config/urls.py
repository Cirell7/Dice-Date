
from django.contrib import admin
from django.urls import path

from django.contrib.auth.views import LoginView
import pages.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', pages.views.main_menu,name='main_menu'),
    path('main', pages.views.maintwo_menu,name='maintwo_menu'),
    path('submit-error/', pages.views.submit_error, name='submit_error'),
    path("register/", pages.views.register_page, name="register"),
    path(
        "login/",
        LoginView.as_view(
            template_name="auth/login.html", next_page=pages.views.profile_page
        ),
        name="login",
    ),
    path("logout/", pages.views.logout_view, name="logout"),
    path("profile/", pages.views.profile_page, name="profile"),
    path("profile_onboarding/", pages.views.profile_page_onboarding, name="profile_page_onboarding"),
    path("add_post/", pages.views.add_post, name="add_post"),
]