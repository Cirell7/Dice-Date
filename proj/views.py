from django.shortcuts import render,redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from proj.models import Form_error
from proj.form import RegisterForm
from django.db.models import QuerySet
from django.contrib.auth import login, logout

# views.py
def profile_page(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect("login")
    
    show_onboarding = request.session.get('new_user', False)
    
    # Удаляем флаг после первого использования
    #if show_onboarding:
    #    del request.session['new_user']
    #    request.session.modified = True
    
    context = {
        "user": request.user,
        "show_onboarding": show_onboarding
    }
    return render(request, "pages/profile.html", context)


# views.py
def register_page(request: HttpRequest) -> HttpResponse:
    error_input = 0
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            # Явно сохраняем сессию с флагом нового пользователя
            request.session['new_user'] = True
            request.session.save()  # Явно сохраняем
            
            return redirect('profile')
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
    return render(request, "pages/hero.html")

def maintwo_menu(request):
    return render(request, "pages/main.html")

def submit_error(request):
    if request.method == "POST":
        error = request.POST.get("error")
        email = request.POST.get("email")
        if error and error.strip():
            Form_error.objects.create(error=error, email=email)
            # Показываем ту же страницу с флагом успеха
            return render(request, 'pages/hero.html', {'show_success': True})

    return redirect('main_menu')