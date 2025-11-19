from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# Импорты из PAGES - ВСЕ onboarding и profile_page тут!
from pages.views import (
    main_menu, maintwo_menu, add_post, post_list, 
    post_detail, post_edit, profile_page_onboarding1,  # ← ОНИ В PAGES!
    profile_page_onboarding2              # ← И profile_page тоже в PAGES!
)

# Импорты из CORE - только аутентификация
from core.views import CustomLoginView, register_page, logout_view, check_username, submit_error

# Импорты из DASHBOARD - только то что реально есть в dashboard
from dashboard.views import (
    messages_list, message_thread, send_message, profile_view,profile_page
    # НЕТ profile_page_onboarding1, profile_page_onboarding2, profile_page!
)
urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Pages URLs
    path('', main_menu, name='main_menu'),
    path('main/', maintwo_menu, name='maintwo_menu'),
    path("add_post/", add_post, name="add_post"),
    path('post_list/', post_list, name='post_list'),
    path('post_detail/<int:post_id>/', post_detail, name='post_detail'),
    path('post_edit/<int:post_id>/', post_edit, name='post_edit'),
    
    # Core/Auth URLs
    path("register/", register_page, name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path('api/check-username/', check_username, name='check_username'),
    path('submit-error/', submit_error, name='submit_error'),
    
    # Dashboard URLs
    path("profile/<int:user_id>/", profile_page, name="profile"),
    path("profile_onboarding1/", profile_page_onboarding1, name="profile_page_onboarding1"),
    path("profile_onboarding2/", profile_page_onboarding2, name="profile_page_onboarding2"),
    path('messages/', messages_list, name='messages_list'),
    path('messages/<int:user_id>/', message_thread, name='message_thread'),
    path('messages/send/<int:post_id>/', send_message, name='send_message'),
    path('profile_view/<int:user_id>/', profile_view, name='profile_view'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)