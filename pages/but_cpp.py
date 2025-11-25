import subprocess
import os
from django.conf import settings
from django.http import HttpResponse

from django.shortcuts import render
from django.conf import settings

from django.shortcuts import render
import subprocess
import os
from django.conf import settings

def games(request):
    cpp_exe = os.path.join(settings.BASE_DIR, 'pages', 'templates', 'pages', 'games.exe')
    
    # Собираем все GET параметры для C++
    args = [cpp_exe]
    for key, value in request.GET.items():
        args.extend([key, str(value)])
    
    try:
        # Запускаем C++ программу
        result = subprocess.run(
            args,
            capture_output=True, 
            text=True, 
            encoding='utf-8',
            timeout=10
        )
        
        # Рендерим шаблон с выводом C++
        return render(request, 'pages/games.html', {
            'game_content': result.stdout
        })
        
    except Exception as e:
        return render(request, 'pages/games.html', {
            'game_content': f'<div class="error">Ошибка: {str(e)}</div>'
        })