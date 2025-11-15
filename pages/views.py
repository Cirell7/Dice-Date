"""pages"""
import datetime

from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse

from pages.models import Posts, Form_error, Profile, Comment
from pages.form import RegisterForm

class CustomLoginView(LoginView):
    """Переопределяет стандартный LoginView для перенаправления"""
    template_name = "auth/login.html"
    def get_success_url(self):
        return f'/profile/{self.request.user.id}'

def profile_page_onboarding1(request: HttpRequest) -> HttpResponse:
    """Настройка предпочтений пользователя при первом входе"""
    if request.method == "POST":
        profile = get_object_or_404(Profile, user_id=request.user)
        verification = Verification(profile, 'gender')
        profile_save, error, profile = verification.verification(request.POST.get('gender'))

        if error!=0:
            messages.error(request, error)
            return JsonResponse({'success': True, 'error': 1})

        if profile_save:
            profile.save()
            profile.user.save()
            return redirect('profile_page_onboarding2')
    return render(request, "pages/onboarding1.html")

def profile_page_onboarding2(request: HttpRequest) -> HttpResponse:
    """Настройка предпочтений пользователя при первом входе"""
    if request.method == "POST":
        profile = get_object_or_404(Profile, user_id=request.user)
        verification = Verification(profile, 'birth_date')
        profile_save, error, profile = verification.verification(request.POST.get('birth_date'))
        if error!=0:
            messages.error(request, error)
            return JsonResponse({'success': True, 'error': 1})
        if profile_save:
            profile.save()
            profile.user.save()
            return redirect('profile',user_id=request.user.id)
    return render(request, "pages/onboarding2.html")


class Verification:
    """Работа с профилем перед сохранением"""
    def __init__(self,profile, field_name):
        self.profile=profile
        self.field_name=field_name

    def verification(self, new):
        profile_save = False
        error=0
        if self.field_name == 'username' and new and new != self.profile.user.username:
            result = self.name_verification(new)
            if result!=new:
                error = result
            self.profile.user.username = new
            profile_save = True

        elif self.field_name == 'gender' and new is not None:
            self.profile.gender = new
            profile_save = True

        elif self.field_name == 'birth_date' and new:
            result = self.day_verification(int(new[:4]))
            if not str(result).isdigit():
                error = result
            self.profile.birth_date = new
            profile_save = True

        elif self.field_name == 'description' and new is not None:
            self.profile.description = new
            profile_save = True

        return profile_save, error, self.profile

    def name_verification(self, new_username):
        """Валидация юзернейма"""
        if len(new_username) < 3 or len(new_username) > 15:
            return 'username_incorrect'
        if User.objects.filter(username=new_username).exists():
            return 'username_exists'
        return new_username

    def day_verification(self, birth_year):
        """Валидация даты рождения"""
        if birth_year > 2008:
            return 'date_error'
        return birth_year


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
            new = request.POST.get(field_name)

            verification = Verification(profile, field_name)
            profile_save, error, profile = verification.verification(new)
            if error!=0:
                messages.error(request, error)
                return JsonResponse({'success': True, 'error': 1})

            if profile_save:
                profile.save()
                profile.user.save()

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
            return redirect('profile_page_onboarding1')
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
    if request.method == 'POST':
        post = Posts(
            name=request.POST['title'],
            description=request.POST.get('description', ''),
            expiration_date=request.POST['event_date'],
            address=request.POST.get('address', ''),
            max_participants=request.POST.get('max_participants', 10),
            user=request.user
        )
        
        if 'image' in request.FILES:
            post.image = request.FILES['image']
            
        post.save()
        return redirect('posts_list')
    
    return render(request, 'pages/add_post.html')

def posts_list(request):
    """Страница со всеми постами"""
    posts = Posts.objects.filter(expiration_date__gte=timezone.now()).order_by('-creation_date')
    
    context = {
        'posts': posts,
        'title_page': 'Все встречи'
    }
    return render(request, 'pages/posts_list.html', context)


def post_detail(request, post_id):
    """Детальный просмотр поста с комментариями"""
    post = get_object_or_404(Posts, id=post_id)
    comments = Comment.objects.filter(post=post).order_by('-created_at')
    
    # Обработка POST-запроса для комментариев
    if request.method == "POST" and request.user.is_authenticated:
        action = request.POST.get("action")
        # Удаление комментария
        if action == "delete_comment":
            comment_id = request.POST.get("comment_id")
            try:
                comment = Comment.objects.get(id=comment_id, user=request.user)
                comment.delete()
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': True})
                return redirect('post_detail', id=post_id)
            except Comment.DoesNotExist:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'error': 'Комментарий не найден'})
        
        # Добавление комментария
        elif 'comment_description' in request.POST and request.POST['comment_description'].strip():
            comment_text = request.POST['comment_description'].strip()
            Comment.objects.create(
                post=post,  # используем post вместо voting
                user=request.user,
                text=comment_text,
            )
            return redirect('post_detail', id=post_id)
    
    context = {
        "post": post,
        "comments": comments,
        "title_page": post.name,
        "user": request.user,
        "user_is_authenticated": request.user.is_authenticated,
    }
    return render(request, "pages/post_detail.html", context)