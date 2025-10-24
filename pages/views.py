from django.shortcuts import render,redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from pages.models import Post, Posts, Form_error, Profile
from pages.form import RegisterForm
from django.db.models import QuerySet
from django.contrib.auth import login, logout


def profile_page_onboarding(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        gender = request.POST.get('gender')
        birth_date = request.POST.get('birth_date')
        
        # Создаем профиль
        
        profile = Profile.objects.create(
            user=request.user,
            gender=gender,
            birth_date=birth_date
        )

        
        profile.save()
        return redirect('profile')
    
    return render(request, "pages/onboarding.html")

def profile_page(request: HttpRequest) -> HttpResponse:
    return render(request, "pages/profile.html")


def register_page(request: HttpRequest) -> HttpResponse:
    error_input = 0
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile_page_onboarding')
        else:
            error_input = 1
    else:
        form = RegisterForm()

    context = {"form": form, "error": error_input, "user": request.user}
    return render(request, "auth/register.html", context)

def logout_view(request):
    logout(request)
    return redirect("main_menu")


def main_menu(request):
    return render(request, "pages/main.html")

def maintwo_menu(request):
    return render(request, "pages/main2.html")

def submit_error(request):
    
    if request.method == "POST":
        error = request.POST.get("error")
        email = request.POST.get("email")
        if error and error.strip():
            Form_error.objects.create(error=error, email=email)
            # Показываем ту же страницу с флагом успеха
            return render(request, 'pages/main.html', {'show_success': True})

    return redirect('main_menu')


from django.contrib import messages
from django.utils import timezone
import datetime

def add_post(request):
    """Создание нового поста"""
    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == "POST":
        try:
            # Извлекаем данные
            name = request.POST.get("voting_name", "").strip()
            description = request.POST.get("voting_description", "").strip()
            post_type = request.POST.get("voting_type", "-1")
            expiration_date = request.POST.get("voting_expiration_date")

            # Проверяем обязательные поля
            if not name or not description or post_type == "-1" or not expiration_date:
                messages.error(request, "Все обязательные поля должны быть заполнены")
            else:
                # Создаем пост
                post = Posts(
                    name=name,
                    description=description,
                    type=int(post_type),
                    creation_date=timezone.now(),
                    expiration_date=expiration_date,
                    user=request.user,
                    image=request.FILES.get("voting_image")
                )
                post.save()

                # Создаем связь в модели Post
                Post.objects.create(
                    past=post,
                    user=request.user,
                    creation_date=timezone.now()
                )

                # Обрабатываем варианты (если есть)
                option_fields = [key for key in request.POST.keys() if key.startswith("option")]
                for field_name in option_fields:
                    option_value = request.POST[field_name].strip()
                    if option_value:
                        # Здесь можно создать варианты если нужно
                        pass

                messages.success(request, "Пост успешно создан!")
                return redirect(f"/posts/{post.id}")

        except Exception as e:
            messages.error(request, "Произошла ошибка при создании поста")

    # GET-запрос или ошибка
    tomorrow = timezone.now() + datetime.timedelta(days=1)
    context = {
        "user": request.user, 
        "tomorrow": tomorrow.strftime("%Y-%m-%dT%H:%M")
    }
    return render(request, "pages/add_post.html", context)
