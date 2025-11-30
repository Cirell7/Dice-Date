from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime

from pages.models import Posts, Comment, PostRequest, PostParticipant  # Добавлены новые модели
from core.models import Profile, Notification
from core.utils import Verification

def main_menu(request):
    """Главная страница"""
    return render(request, "pages/main.html")


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
        # Проверяем дату (только формат)
        event_date = request.POST['event_date']
        
        try:
            _ = datetime.fromisoformat(event_date.replace('Z', '+00:00'))
        except ValueError:
            pass
        
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
            longitude=longitude,
            is_active=True
        )

        post.save()
        return redirect('post_list')
    
    return render(request, 'pages/add_post.html')

def post_list(request):
    """Страница со всеми постами"""
    posts = Posts.objects.filter(
        expiration_date__gte=timezone.now(),
        is_active=True
    ).order_by('-creation_date')
    
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
