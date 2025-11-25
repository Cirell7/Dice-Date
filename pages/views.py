from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from pages.models import Posts, Comment, PostRequest, PostParticipant  # Добавлены новые модели
from core.models import Profile, Notification
from core.utils import Verification

def main_menu(request):
    """Главная страница"""
    return render(request, "pages/main.html")

import subprocess
import os
from django.conf import settings
import subprocess
import os
from django.conf import settings
from django.http import HttpResponse

import subprocess
import os
import tempfile
from django.conf import settings
from django.http import HttpResponse

def games(request):
    """Компиляция и выполнение C++ кода"""
    
    # Получаем координаты из GET параметров
    x = request.GET.get('x')
    y = request.GET.get('y')
    
    # Создаем временный C++ файл с правильным экранированием
    cpp_code = '''#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>

using namespace std;

class Minesweeper {
private:
    vector<vector<char>> board;
    vector<vector<bool>> mines;
    vector<vector<bool>> revealed;
    int size;
    int mineCount;
    bool gameOver;
    bool gameWon;

public:
    Minesweeper(int n, int minesCount) : size(n), mineCount(minesCount), gameOver(false), gameWon(false) {
        board.resize(size, vector<char>(size, ' '));
        mines.resize(size, vector<bool>(size, false));
        revealed.resize(size, vector<bool>(size, false));
        placeMines();
        calculateNumbers();
    }

    void placeMines() {
        srand(time(0));
        int placed = 0;
        while (placed < mineCount) {
            int x = rand() % size;
            int y = rand() % size;
            if (!mines[x][y]) {
                mines[x][y] = true;
                placed++;
            }
        }
    }

    void calculateNumbers() {
        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
                if (!mines[i][j]) {
                    int count = 0;
                    for (int dx = -1; dx <= 1; dx++) {
                        for (int dy = -1; dy <= 1; dy++) {
                            int ni = i + dx, nj = j + dy;
                            if (ni >= 0 && ni < size && nj >= 0 && nj < size && mines[ni][nj]) {
                                count++;
                            }
                        }
                    }
                    if (count > 0) {
                        board[i][j] = '0' + count;
                    }
                }
            }
        }
    }

    void reveal(int x, int y) {
        if (x < 0 || x >= size || y < 0 || y >= size || revealed[x][y] || gameOver || gameWon) {
            return;
        }

        revealed[x][y] = true;

        if (mines[x][y]) {
            gameOver = true;
            return;
        }

        if (board[x][y] == ' ') {
            for (int dx = -1; dx <= 1; dx++) {
                for (int dy = -1; dy <= 1; dy++) {
                    reveal(x + dx, y + dy);
                }
            }
        }

        checkWin();
    }

    void checkWin() {
        int unrevealedSafe = 0;
        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
                if (!revealed[i][j] && !mines[i][j]) {
                    unrevealedSafe++;
                }
            }
        }
        gameWon = (unrevealedSafe == 0);
    }

    void display() {
        cout << "<div class='minesweeper-game'>";
        cout << "<div class='game-status'>";
        if (gameOver) {
            cout << "<div class='status game-over'>💥 Игра окончена! Вы проиграли!</div>";
        } else if (gameWon) {
            cout << "<div class='status game-won'>🎉 Поздравляем! Вы выиграли!</div>";
        } else {
            cout << "<div class='status playing'>🎮 Игра идет...</div>";
        }
        cout << "</div>";

        cout << "<div class='game-board'>";
        for (int i = 0; i < size; i++) {
            cout << "<div class='row'>";
            for (int j = 0; j < size; j++) {
                if (gameOver && mines[i][j]) {
                    cout << "<div class='cell mine'>💣</div>";
                } else if (revealed[i][j]) {
                    if (board[i][j] == ' ') {
                        cout << "<div class='cell revealed'></div>";
                    } else {
                        cout << "<div class='cell revealed number-" << board[i][j] << "'>" << board[i][j] << "</div>";
                    }
                } else {
                    cout << "<a href='/games?x=" << i << "&y=" << j << "' class='cell hidden'>?</a>";
                }
            }
            cout << "</div>";
        }
        cout << "</div>";

        cout << "<div class='game-controls'>";
        cout << "<a href='/games' class='btn new-game'>🔄 Новая игра</a>";
        cout << "</div>";
        cout << "</div>";
    }
};

int main() {
    // Устанавливаем заголовок HTML
    cout << "Content-Type: text/html; charset=utf-8\\\\n\\\\n";
    
    cout << "<!DOCTYPE html>";
    cout << "<html lang='ru'>";
    cout << "<head>";
    cout << "<meta charset='UTF-8'>";
    cout << "<meta name='viewport' content='width=device-width, initial-scale=1.0'>";
    cout << "<title>Сапер на C++</title>";
    cout << "<style>";
    cout << "* { margin: 0; padding: 0; box-sizing: border-box; }";
    cout << "body { font-family: 'Courier New', monospace; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color: white; min-height: 100vh; display: flex; flex-direction: column; align-items: center; padding: 20px; }";
    cout << ".container { max-width: 600px; width: 100%; text-align: center; }";
    cout << ".header { margin-bottom: 30px; }";
    cout << ".header h1 { font-size: 2.5em; color: #00ff88; text-shadow: 0 0 10px rgba(0, 255, 136, 0.5); margin-bottom: 10px; }";
    cout << ".minesweeper-game { background: rgba(255, 255, 255, 0.1); border-radius: 15px; padding: 20px; border: 1px solid rgba(255, 255, 255, 0.2); backdrop-filter: blur(10px); }";
    cout << ".game-status { margin-bottom: 20px; }";
    cout << ".status { font-size: 1.2em; font-weight: bold; padding: 10px; border-radius: 8px; }";
    cout << ".game-over { background: rgba(255, 0, 0, 0.3); color: #ff6b6b; }";
    cout << ".game-won { background: rgba(0, 255, 0, 0.3); color: #51ff00; }";
    cout << ".playing { background: rgba(0, 150, 255, 0.3); color: #00a8ff; }";
    cout << ".game-board { display: inline-block; margin: 20px 0; }";
    cout << ".row { display: flex; }";
    cout << ".cell { width: 40px; height: 40px; margin: 2px; display: flex; align-items: center; justify-content: center; border-radius: 5px; cursor: pointer; font-weight: bold; transition: all 0.3s ease; text-decoration: none; color: white; }";
    cout << ".hidden { background: rgba(255, 255, 255, 0.2); border: 2px solid rgba(255, 255, 255, 0.3); }";
    cout << ".hidden:hover { background: rgba(255, 255, 255, 0.3); transform: scale(1.05); }";
    cout << ".revealed { background: rgba(255, 255, 255, 0.1); border: 1px solid rgba(255, 255, 255, 0.1); }";
    cout << ".mine { background: rgba(255, 0, 0, 0.3); font-size: 1.2em; }";
    cout << ".number-1 { color: #00ff88; }";
    cout << ".number-2 { color: #ffd700; }";
    cout << ".number-3 { color: #ff6b6b; }";
    cout << ".number-4 { color: #a855f7; }";
    cout << ".number-5 { color: #ff8c00; }";
    cout << ".number-6 { color: #00ced1; }";
    cout << ".number-7 { color: #ff1493; }";
    cout << ".number-8 { color: #7cfc00; }";
    cout << ".game-controls { margin-top: 20px; }";
    cout << ".btn { background: linear-gradient(135deg, #00ff88 0%, #00a8ff 100%); color: #1a1a2e; border: none; padding: 12px 24px; border-radius: 25px; font-size: 1.1em; font-weight: bold; cursor: pointer; transition: all 0.3s ease; font-family: 'Courier New', monospace; text-decoration: none; display: inline-block; }";
    cout << ".btn:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0, 255, 136, 0.4); }";
    cout << ".instructions { margin-top: 30px; background: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 10px; text-align: left; }";
    cout << ".instructions h3 { color: #00ff88; margin-bottom: 10px; }";
    cout << ".instructions ul { list-style-position: inside; }";
    cout << ".instructions li { margin: 5px 0; }";
    cout << "</style>";
    cout << "</head>";
    cout << "<body>";
    cout << "<div class='container'>";
    cout << "<div class='header'>";
    cout << "<h1>🎮 Сапер на C++</h1>";
    cout << "<p>Классическая игра, полностью написанная на C++</p>";
    cout << "</div>";

    // Создаем игру
    Minesweeper game(8, 10);
    ''' + (f'game.reveal({x}, {y});' if x and y else '') + '''
    
    // Отображаем игровое поле
    game.display();

    cout << "<div class='instructions'>";
    cout << "<h3>📋 Правила игры:</h3>";
    cout << "<ul>";
    cout << "<li>Нажмите на клетку, чтобы открыть её</li>";
    cout << "<li>Цифра показывает количество мин вокруг клетки</li>";
    cout << "<li>Избегайте мин 💣</li>";
    cout << "<li>Откройте все безопасные клетки, чтобы выиграть!</li>";
    cout << "</ul>";
    cout << "</div>";
    cout << "</div>";
    cout << "</body>";
    cout << "</html>";
    
    return 0;
}'''
    
    try:
        # Создаем временный файл
        with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', delete=False, encoding='utf-8') as f:
            f.write(cpp_code)
            cpp_file_path = f.name
        
        # Компилируем
        executable_path = cpp_file_path.replace('.cpp', '.exe')
        compile_result = subprocess.run([
            'g++', '-std=c++11', cpp_file_path, '-o', executable_path
        ], capture_output=True, text=True, timeout=30)
        
        if compile_result.returncode != 0:
            # Если компиляция не удалась, показываем простую HTML страницу
            simple_html = '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Сапер</title>
                <style>
                    body { font-family: Arial; padding: 20px; }
                    .cell { width: 30px; height: 30px; border: 1px solid #000; display: inline-block; margin: 2px; text-align: center; line-height: 30px; }
                </style>
            </head>
            <body>
                <h1>Сапер (упрощенная версия)</h1>
                <p>К сожалению, компиляция C++ кода не удалась.</p>
                <p>Ошибка: ''' + compile_result.stderr + '''</p>
                <div>
                    <a href="/games">Новая игра</a>
                </div>
            </body>
            </html>
            '''
            return HttpResponse(simple_html, content_type='text/html; charset=utf-8')
        
        # Запускаем
        exec_result = subprocess.run([executable_path], capture_output=True, text=True, timeout=10)
        
        if exec_result.returncode == 0:
            return HttpResponse(exec_result.stdout, content_type='text/html; charset=utf-8')
        else:
            return HttpResponse(f"Ошибка выполнения: {exec_result.stderr}", status=500)
            
    except Exception as e:
        return HttpResponse(f"Ошибка: {str(e)}", status=500)
    finally:
        # Удаляем временные файлы
        try:
            if 'cpp_file_path' in locals() and os.path.exists(cpp_file_path):
                os.remove(cpp_file_path)
            if 'executable_path' in locals() and os.path.exists(executable_path):
                os.remove(executable_path)
        except:
            pass

def maintwo_menu(request):
    """Страница с информацией о проекте"""
    return render(request, "pages/main2.html")

@login_required
def profile_page_onboarding1(request: HttpRequest) -> HttpResponse:
    """Настройка предпочтений пользователя при первом входе"""
    if request.method == "POST":
        profile = get_object_or_404(Profile, user_id=request.user)
        verification = Verification(profile, 'gender')
        profile_save, error, profile = verification.verification(request.POST.get('gender'))

        if error != 0:
            messages.error(request, error)
            return JsonResponse({'success': True, 'error': 1})

        if profile_save:
            profile.save()
            profile.user.save()
            return redirect('profile_page_onboarding2')
    return render(request, "pages/onboarding1.html")

@login_required
def profile_page_onboarding2(request: HttpRequest) -> HttpResponse:
    """Настройка предпочтений пользователя при первом входе"""
    if request.method == "POST":
        profile = get_object_or_404(Profile, user_id=request.user)
        verification = Verification(profile, 'birth_date')
        profile_save, error, profile = verification.verification(request.POST.get('birth_date'))
        if profile_save and error == 0:
            profile.save()
            profile.user.save()
            return redirect('post_list')
        elif profile_save:
            return redirect('post_list')
    return render(request, "pages/onboarding2.html")

@login_required
def add_post(request):
    """Создание нового поста"""
    if request.method == 'POST':
        latitude_str = request.POST.get('latitude', '').strip()
        longitude_str = request.POST.get('longitude', '').strip()
        
        latitude = None
        longitude = None
        
        if latitude_str and longitude_str:
            try:
                latitude = float(latitude_str)
                longitude = float(longitude_str)
            except (ValueError, TypeError):
                pass
        
        post = Posts(
            name=request.POST['title'],
            description=request.POST.get('description', ''),
            expiration_date=request.POST['event_date'],
            address=request.POST.get('address', ''),
            max_participants=request.POST.get('max_participants', 10),
            user=request.user,
            latitude=latitude,
            longitude=longitude
        )

        post.save()
        return redirect('post_list')
    
    return render(request, 'pages/add_post.html')

def post_list(request):
    """Страница со всеми постами"""
    posts = Posts.objects.filter(expiration_date__gte=timezone.now()).order_by('-creation_date')
    
    context = {
        'posts': posts,
        'title_page': 'Все встречи'
    }
    return render(request, 'pages/post_list.html', context)

@login_required
def post_detail(request, post_id):
    """Детальный просмотр поста с комментариями"""
    post = get_object_or_404(Posts, id=post_id)
    comments = Comment.objects.filter(post=post).order_by('-created_at')
    
    # Добавляем логику для проверки статуса пользователя
    user_has_pending_request = False
    user_is_approved = False
    is_full = False
    
    user_has_pending_request = PostRequest.objects.filter(
        post=post, 
        user=request.user, 
        status='pending'
    ).exists()
        
        # Проверяем, является ли пользователь одобренным участником
    user_is_approved = PostParticipant.objects.filter(
        post=post, 
        user=request.user
    ).exists()
        
        # Проверяем, достигнут ли лимит участников
    current_participants = PostParticipant.objects.filter(post=post).count()
    is_full = current_participants >= post.max_participants
    
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "delete_comment":
            comment_id = request.POST.get("comment_id")
            try:
                comment = Comment.objects.get(id=comment_id, user=request.user)
                comment.delete()
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': True})
                return redirect('post_detail', post_id=post_id)
            except Comment.DoesNotExist:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'error': 'Комментарий не найден'})
        
        elif 'comment_description' in request.POST and request.POST['comment_description'].strip():
            comment_text = request.POST['comment_description'].strip()
            Comment.objects.create(
                post=post,
                user=request.user,
                text=comment_text,
            )
            return redirect('post_detail', post_id=post_id)
    
    context = {
        "post": post,
        "comments": comments,
        "title_page": post.name,
        "user": request.user,
        "user_has_pending_request": user_has_pending_request,
        "user_is_approved": user_is_approved,
        "is_full": is_full,
        "approved_participants_count": PostParticipant.objects.filter(post=post).count(),
        "pending_requests_count": PostRequest.objects.filter(post=post, status='pending').count(),
    }
    return render(request, "pages/post_detail.html", context)

@login_required
def post_edit(request: HttpRequest, post_id) -> HttpResponse:
    post = get_object_or_404(Posts, id=post_id)
    
    if request.method == "POST":
        action = request.POST.get('action')
        
        if action == 'delete':
            post.delete()
            return redirect('post_list') 
        
        elif action == 'submit':
            post.name = request.POST['post_name']
            post.description = request.POST.get('post_description', '')
            post.expiration_date = request.POST['post_expiration_date']
            post.address = request.POST.get('post_address', '')
            post.max_participants = request.POST.get('post_max_participants', 10)
            
            if 'post_image' in request.FILES:
                post.image = request.FILES['post_image']
            
            post.save()
            return redirect('post_detail', post_id=post_id)
    
    context = {'post': post}
    return render(request, "pages/post_edit.html", context)

@login_required
def join_post(request, post_id):
    """Обработка заявки на участие в мероприятии"""
    if request.method == 'POST':
        post = get_object_or_404(Posts, id=post_id)
        PostRequest.objects.create(post=post, user=request.user)
        
        # Создаем уведомление для автора поста
        Notification.objects.create(
            user=post.user,
            title="Новая заявка на участие",
            message=f"Пользователь {request.user.username} хочет присоединиться к вашему мероприятию '{post.name}'",
            notification_type='join_request'
        )
    return redirect('post_detail', post_id=post_id)

@login_required
def post_requests(request, post_id):
    """Страница с заявками на участие"""
    post = get_object_or_404(Posts, id=post_id)
    
    # Проверяем, что пользователь - автор поста
    if request.user != post.user:
        return redirect('post_detail', post_id=post_id)
    
    pending_requests = PostRequest.objects.filter(post=post, status='pending')
    
    return render(request, 'pages/post_requests.html', {
        'post': post,
        'pending_requests': pending_requests,
    })

@login_required
def approve_request(request, post_id, request_id):
    """Одобрение заявки на участие"""
    if request.method == 'POST':
        post_request = get_object_or_404(PostRequest, id=request_id, post_id=post_id)
        
        # Проверяем, что пользователь - автор поста
        if request.user != post_request.post.user:
            return redirect('post_detail', post_id=post_id)
        
        # Проверяем, есть ли свободные места
        current_participants = PostParticipant.objects.filter(post=post_request.post).count()
        if current_participants >= post_request.post.max_participants:
            messages.error(request, "Достигнут лимит участников")
            return redirect('post_requests', post_id=post_id)
        
        # Одобряем заявку
        post_request.status = 'approved'
        post_request.save()
        
        # Добавляем пользователя в участники
        PostParticipant.objects.create(post=post_request.post, user=post_request.user)
        
        # Создаем уведомление для пользователя
        Notification.objects.create(
            user=post_request.user,
            title="Заявка одобрена",
            message=f"Ваша заявка на участие в мероприятии '{post_request.post.name}' была одобрена!",
            notification_type='request_approved'
        )

    return redirect('post_requests', post_id=post_id)

@login_required
def reject_request(request, post_id, request_id):
    """Отклонение заявки на участие"""
    if request.method == 'POST':
        post_request = get_object_or_404(PostRequest, id=request_id, post_id=post_id)
        
        # Проверяем, что пользователь - автор поста
        if request.user != post_request.post.user:
            return redirect('post_detail', post_id=post_id)
        
        # Отклоняем заявку
        post_request.status = 'rejected'
        post_request.save()
        
        # Создаем уведомление для пользователя
        Notification.objects.create(
            user=post_request.user,
            title="Заявка отклонена",
            message=f"Ваша заявка на участие в мероприятии '{post_request.post.name}' была отклонена",
            notification_type='request_rejected'
        )
    return redirect('post_requests', post_id=post_id)
