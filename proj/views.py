from django.shortcuts import render,redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from proj.models import Form,Form_error
from proj.form import RegisterForm
from django.db.models import QuerySet
from django.contrib.auth import login, logout

# Create your views here.
def profile_page(request: HttpRequest) -> HttpResponse:
    """
    страница профиля
    """
    if not request.user.is_authenticated:
        return redirect("login")
    context: dict[str, str | QuerySet] = {"user": request.user}
    return render(request, "pages/profile.html", context)

def register_page(request: HttpRequest) -> HttpResponse:
    """
    страница и API регистрации

    если `POST`-запрос - регистрирует пользователя
    если нет - возвращает страницу
    """
    error_input = 0
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(profile_page)
        else:
            error_input = 1
    else:
        form = RegisterForm()

    context = {"form": form, "error": error_input, "user": request.user}
    return render(request, "auth/register.html", context)


def logout_view(request):
    logout(request)
    return redirect("index")


def main_menu(request):
    return render(request, "hero.html")

def maintwo_menu(request):
    return render(request, "main.html")

def submit_error(request):
    if request.method == "POST":
        error = request.POST.get("error")
        email = request.POST.get("email")
        if error and error.strip():
            Form_error.objects.create(error=error, email=email)
            # Показываем ту же страницу с флагом успеха
            return render(request, 'hero.html', {'show_success': True})
    
    return redirect('main_menu')