"""pages"""
import datetime

from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse

from pages.models import Post, Posts, Form_error, Profile
from pages.form import RegisterForm

class CustomLoginView(LoginView):
    """Переопределяет стандартный LoginView для перенаправления"""
    template_name = "auth/login.html"
    def get_success_url(self):
        return f'/profile/{self.request.user.id}'

def profile_page_onboarding(request: HttpRequest) -> HttpResponse:
    """Настройка предпочтений пользователя при первом входе"""
    if request.method == "POST":
        gender = request.POST.get('gender')
        birth_date = request.POST.get('birth_date')

        profile = Profile.objects.get(user=request.user)
        profile.gender = gender
        profile.birth_date = birth_date
        profile.save()

        return redirect('profile',user_id=request.user.id)
    return render(request, "pages/onboarding.html")

def profile_page(request: HttpRequest, user_id) -> HttpResponse:
    """Профиль пользователя"""
    profile = get_object_or_404(Profile, user_id=user_id)

    if request.method == 'POST':
        # Обработка загрузки фото
        if 'update_photo' in request.POST and request.FILES.get('photo'):
            profile.photo = request.FILES['photo']
            profile.save()
            return redirect('profile', user_id=user_id)

        # AJAX запрос на обновление поля
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            field_name = request.POST.get('update_field')
            profile_save = False

            if field_name == 'username':
                new_username = request.POST.get('username')
                if len(new_username) < 3 or len(new_username) > 15:
                    messages.error(request, 'username_incorrect')
                    return JsonResponse({'success': True, 'error': 1})
                if User.objects.filter(username=new_username).exists():
                    messages.error(request, 'username_exists')
                    return JsonResponse({'success': True, 'error': 1})
                if new_username and new_username != profile.user.username:
                    profile.user.username = new_username
                    profile_save = True

            elif field_name == 'gender':
                new_gender = request.POST.get('gender')
                if new_gender is not None:
                    profile.gender = new_gender
                    profile_save = True

            elif field_name == 'birth_date':
                birth_date = request.POST.get('birth_date')
                if birth_date:
                    birth_year = int(birth_date[:4])
                    if birth_year > 2008:
                        messages.error(request, 'date_error')
                        return JsonResponse({'success': True, 'error': 1})
                    profile.birth_date = birth_date
                    profile_save = True

            elif field_name == 'description':
                new_description = request.POST.get('description')
                if new_description is not None:
                    profile.description = new_description
                    profile_save = True
            if profile_save:
                profile.save()

            return JsonResponse({'success': True, 'error': 0})

    context = {
        "profile": profile,
        "user": profile.user,
    }
    return render(request, "pages/profile.html", context)

def check_username(request):
    """API для проверки уникальности username"""
    username = request.GET.get('username', '').strip()
    exists = User.objects.filter(username__iexact=username).exists()
    return JsonResponse({'available': not exists})

def register_page(request: HttpRequest) -> HttpResponse:
    """Регистрация пользователя"""
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            Profile.objects.create(user=user)
            return redirect('profile_page_onboarding')
    else:
        form = RegisterForm()

    context = {"form": form, "user": request.user}
    return render(request, "auth/register.html", context)

def logout_view(request):
    """Вход в аккаунт"""
    logout(request)
    return redirect("main_menu")

def main_menu(request):
    """Главная страница"""
    return render(request, "pages/main.html")

def maintwo_menu(request):
    """Страница с информацией о проекте"""
    return render(request, "pages/main2.html")

def submit_error(request):
    """Форма сообщения об ошибке"""
    if request.method == "POST":
        error = request.POST.get("error")
        email = request.POST.get("email")
        if error and error.strip():
            Form_error.objects.create(error=error, email=email)
            # Показываем ту же страницу с флагом успеха
            return render(request, 'pages/main.html', {'show_success': True})

    return redirect('main_menu')

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
