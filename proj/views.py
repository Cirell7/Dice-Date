from django.shortcuts import render,redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from proj.models import Form,Form_error
# Create your views here.
def form_menu(request):
    operation1 = request.GET.get("operation",0)
    Form(operation=operation1).save()
    data = Form.objects.all()
    conext = {"data": data}
    return render(request, "2.html")

def main_menu(request):
    return render(request, "main.html")

def submit_error(request):
    if request.method == "POST":
        error = request.POST.get("error")
        email = request.POST.get("email")
        if error:
            Form_error.objects.create(error=error, email=email)
            return redirect('main_menu')  # ← это важно!
    return redirect('main_menu')