from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from pages.models import Posts, PostRequest, PostParticipant
from core.models import Notification, ParticipantRating

@login_required
def join_post(request, post_id):
    """Обработка заявки на участие в мероприятии"""
    if request.method == 'POST':
        post = get_object_or_404(Posts, id=post_id)
        PostRequest.objects.create(post=post, user=request.user)

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

    if request.user != post.user:
        return redirect('post_detail', post_id=post_id)

    pending_requests = PostRequest.objects.filter(post=post, status='pending')

    return render(request, 'notifications/post_requests.html', {
        'post': post,
        'pending_requests': pending_requests,
    })

@login_required
def approve_request(request, post_id, request_id):
    """Одобрение заявки на участие"""
    if request.method == 'POST':
        post_request = get_object_or_404(PostRequest, id=request_id, post_id=post_id)

        if request.user != post_request.post.user:
            return redirect('post_detail', post_id=post_id)

        current_participants = PostParticipant.objects.filter(post=post_request.post).count()
        if current_participants >= post_request.post.max_participants:
            messages.error(request, "Достигнут лимит участников")
            return redirect('post_requests', post_id=post_id)

        post_request.status = 'approved'
        post_request.save()

        PostParticipant.objects.create(post=post_request.post, user=post_request.user)

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

        if request.user != post_request.post.user:
            return redirect('post_detail', post_id=post_id)

        post_request.status = 'rejected'
        post_request.save()

        Notification.objects.create(
            user=post_request.user,
            title="Заявка отклонена",
            message=f"Ваша заявка на участие в мероприятии '{post_request.post.name}' была отклонена",
            notification_type='request_rejected'
        )
    return redirect('post_requests', post_id=post_id)

@login_required
def remove_participant(request, post_id, user_id):
    """Удаление участника из мероприятия"""
    if request.method == 'POST':
        post = get_object_or_404(Posts, id=post_id)

        if request.user != post.user:
            messages.error(request, "У вас нет прав для удаления участников")
            return redirect('post_detail', post_id=post_id)

        participant = get_object_or_404(PostParticipant, post=post, user_id=user_id)

        if participant.user == post.user:
            messages.error(request, "Нельзя удалить автора мероприятия")
            return redirect('post_requests', post_id=post_id)

        username = participant.user.username

        participant.delete()

        if hasattr(post, 'current_participants'):
            post.current_participants = PostParticipant.objects.filter(post=post).count()
            post.save()

        Notification.objects.create(
            user=participant.user,
            title="Вы были удалены из мероприятия",
            message=f"Автор удалил вас из мероприятия '{post.name}'",
            notification_type='removed_from_post'
        )

        messages.success(request, f"Участник {username} удален")

    return redirect('post_requests', post_id=post_id)

def get_next_participant(request, post):
    """Перейти к следующему участнику"""
    people_to_rate = []

    if request.user == post.user:
        participants = PostParticipant.objects.filter(post=post).select_related('user')
        for participant in participants:
            people_to_rate.append(participant.user)
    else:
        people_to_rate.append(post.user)

        participants = PostParticipant.objects.filter(post=post).exclude(user=request.user).select_related('user')
        for participant in participants:
            people_to_rate.append(participant.user)

    for person in people_to_rate:
        if not ParticipantRating.objects.filter(
            post=post,
            rater=request.user,
            participant=person
        ).exists():
            return redirect('rate_participant', event_id=post.id, participant_id=person.id)

    return render(request, 'notifications/rating_complete.html')

@login_required
def rate_participant(request, event_id, participant_id):
    """Оценивание после завершения встречи"""
    post = get_object_or_404(Posts, id=event_id)
    participant = get_object_or_404(User, id=participant_id)

    is_organizer = request.user == post.user
    is_participant = PostParticipant.objects.filter(post=post, user=request.user).exists()

    if not (is_organizer or is_participant):
        return redirect('post_detail', post_id=event_id)

    if participant == request.user:
        return get_next_participant(request, post)

    can_be_rated = False

    if is_organizer:
        can_be_rated = PostParticipant.objects.filter(post=post, user=participant).exists()
    else:
        can_be_rated = (
            participant == post.user or
            PostParticipant.objects.filter(post=post, user=participant).exclude(user=request.user).exists()
        )

    if not can_be_rated:
        return redirect('post_detail', post_id=event_id)

    if ParticipantRating.objects.filter(post=post, rater=request.user, participant=participant).exists():
        return get_next_participant(request, post)

    if request.method == 'POST':
        was_late = request.POST.get('was_late') == 'true'
        would_repeat = request.POST.get('would_repeat') == 'true'

        ParticipantRating.objects.create(
            post=post,
            rater=request.user,
            participant=participant,
            was_late=was_late,
            would_repeat=would_repeat
        )

        return get_next_participant(request, post)

    if is_organizer:
        all_to_rate = PostParticipant.objects.filter(post=post).values_list('user', flat=True)
    else:
        all_to_rate = [post.user]
        other_participants = PostParticipant.objects.filter(post=post).exclude(user=request.user).values_list('user', flat=True)
        all_to_rate.extend(other_participants)

    total_count = len(all_to_rate)

    rated_count = ParticipantRating.objects.filter(post=post, rater=request.user).count()

    context = {
        'post': post,
        'participant': participant,
        'current_number': rated_count + 1,
        'total_count': total_count,
        'is_last': (rated_count + 1) == total_count,
    }
    return render(request, 'notifications/rate_participant.html', context)
