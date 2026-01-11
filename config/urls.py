from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from core.views import (CustomLoginView, register_page, logout_view, check_username, submit_error,
notifications_page,mark_notification_read,
mark_all_notifications_read
)

from dashboard.views import (
    messages_list, message_thread, profile_view, profile_page
)

from notifications.views import (
    join_post, post_requests,
    approve_request, reject_request, rate_participant, remove_participant
)

from pages.views import (
    main_menu, maintwo_menu, add_post, post_list,
    post_detail, post_edit, profile_page_onboarding1,
    profile_page_onboarding2
)


urlpatterns = [
    path('admin/', admin.site.urls),

    # Core/Auth URLs
    path("register/", register_page, name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path('api/check-username/', check_username, name='check_username'),
    path('submit-error/', submit_error, name='submit_error'),
    path('notifications/', notifications_page, name='notifications_page'),
    path('notifications/<int:notification_id>/mark-read/', mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-all-read/', mark_all_notifications_read, name='mark_all_read'),

    # Dashboard URLs
    path("profile/<int:user_id>/", profile_page, name="profile"),
    path('messages/', messages_list, name='messages_list'),
    path('messages/<int:user_id>/', message_thread, name='message_thread'),
    path('profile_view/<int:user_id>/', profile_view, name='profile_view'),

    # Pages URLs
    path('', main_menu, name='main_menu'),
    path('main/', maintwo_menu, name='maintwo_menu'),
    path("add_post/", add_post, name="add_post"),
    path('post_list/', post_list, name='post_list'),
    path('post_detail/<int:post_id>/', post_detail, name='post_detail'),
    path('post_edit/<int:post_id>/', post_edit, name='post_edit'),
    path("profile_onboarding1/", profile_page_onboarding1, name="profile_page_onboarding1"),
    path("profile_onboarding2/", profile_page_onboarding2, name="profile_page_onboarding2"),

    # Notifications URLs
    path('post/<int:post_id>/requests/<int:request_id>/approve/', approve_request, name='approve_request'),
    path('post/<int:post_id>/requests/<int:request_id>/reject/', reject_request, name='reject_request'),
    path('post/<int:post_id>/remove_participant/<int:user_id>/', remove_participant, name='remove_participant'),
    path('event/<int:event_id>/rate-participant/<int:participant_id>/', rate_participant, name='rate_participant'),

    path('post/<int:post_id>/join/', join_post, name='join_post'),
    path('post/<int:post_id>/requests/', post_requests, name='post_requests'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
