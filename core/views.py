# core/views.py
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
    return render(request, "core/register.html", context)  # ← ИСПРАВИТЬ НА "core/register.html"

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
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'core/notifications_page.html', {
        'notifications': notifications
    })