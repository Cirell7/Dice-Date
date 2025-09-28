
from django.contrib import admin
from django.urls import path
import proj.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', proj.views.main_menu,name='main_menu'),
    path('form', proj.views.form_menu),
    path('submit-error/', proj.views.submit_error, name='submit_error'),

]