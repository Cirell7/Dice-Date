from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse

from core.forms import RegisterForm
from core.models import Profile, Form_error, Notification

class CustomLoginView(LoginView):
    template_name = "core/login.html"
    def get_success_url(self):
        return '/post_list/'

def register_page(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            Profile.objects.create(user=user)
            return redirect('profile_page_onboarding1')
    else:
        form = RegisterForm()

    context = {"form": form, "user": request.user}
    return render(request, "core/register.html", context)

def logout_view(request):
    logout(request)
    return redirect("main_menu")

def check_username(request):
    username = request.GET.get('username', '').strip()
    exists = User.objects.filter(username__iexact=username).exists()
    return JsonResponse({'available': not exists})

def submit_error(request):
    if request.method == "POST":
        error = request.POST.get("error")
        email = request.POST.get("email")
        if error and error.strip():
            Form_error.objects.create(error=error, email=email)
            return render(request, 'pages/main.html', {'show_success': True})
    return redirect('main_menu')


def notifications_page(request):
    """Страница со всеми уведомлениями"""
    try:
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')

        unread_notifications_count = Notification.objects.filter(
            user=request.user, 
            is_read=False
        ).count()
        
        recent_notifications = Notification.objects.filter(
            user=request.user
        ).order_by('-created_at')[:5]
        
        context = {
            'notifications': notifications,
            'unread_notifications_count': unread_notifications_count,
            'recent_notifications': recent_notifications,
        }
        
        return render(request, 'core/notifications_page.html', context)
        
    except Exception as e:
        # Обработка ошибок (логирование, возврат пустого контекста и т.д.)
        print(f"Ошибка при загрузке уведомлений: {e}")
        context = {
            'notifications': [],
            'unread_notifications_count': 0,
            'recent_notifications': [],
        }
        return render(request, 'core/notifications_page.html', context)

def mark_notification_read(request, notification_id):
    """Пометить уведомление как прочитанное"""
    try:
        notification = get_object_or_404(Notification, id=notification_id, user=request.user)
        notification.is_read = True
        notification.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def mark_all_notifications_read(request):
    """Пометить все уведомления как прочитанные"""
    try:
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
