from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages

from dashboard.models import Message
from core.models import Profile, User, ParticipantRating
from core.utils import Verification

@login_required
def profile_page(request: HttpRequest, user_id) -> HttpResponse:
    """Профиль пользователя"""
    if user_id!=request.user.id:
        return redirect('profile_view', user_id=user_id)

    profile = get_object_or_404(Profile, user_id=user_id)
    if request.method == 'POST':
        if 'update_photo' in request.POST and request.FILES.get('photo'):
            profile.photo = request.FILES['photo']
            profile.save()
            return redirect('profile', user_id=user_id)

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            field_name = request.POST.get('update_field')
            new = request.POST.get(field_name)
            verification = Verification(profile, field_name)
            profile_save, error, profile = verification.verification(new)
            if error != 0:
                messages.error(request, error)
                return JsonResponse({'success': True, 'error': 1})
            if profile_save:
                profile.save()
                profile.user.save()
            return JsonResponse({'success': True, 'error': 0})

    context = {
        "profile": profile, "user": profile.user,
    }
    return render(request, "dashboard/profile.html", context)

def profile_view(request: HttpRequest, user_id: int):
    """Просмотр чужого профиля"""
    if user_id==request.user.id:
        return redirect('profile', user_id=user_id)

    profile_user = get_object_or_404(User, id=user_id)
    profile, _ = Profile.objects.get_or_create(user=profile_user)

    ratings = ParticipantRating.objects.filter(participant=user_id)

    would_repeat_count = ratings.filter(would_repeat=True).count()
    late_count = ratings.filter(was_late=True).count()

    is_own_profile = request.user.is_authenticated and request.user.id == user_id

    context = {
        'profile_user': profile_user,
        'profile': profile,
        'is_own_profile': is_own_profile,
        'late_count': late_count,
        'would_repeat_count': would_repeat_count
    }

    return render(request, 'dashboard/profile_view.html', context)

@login_required
def messages_list(request: HttpRequest) -> HttpResponse:
    """Список диалогов пользователя"""
    user_messages =  Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).order_by('-timestamp')

    threads = {}
    for message in user_messages:
        if message.sender == request.user:
            other_user = message.receiver
        else:
            other_user = message.sender
        if other_user.id not in threads:
            threads[other_user.id] = {
                'user': other_user,
                'last_message': message,
                'unread_count': Message.objects.filter(sender=other_user, receiver=request.user, is_read=False).count()
            }

    context = {
        'threads': sorted(threads.values(), key=lambda x: x['last_message'].timestamp, reverse=True)
    }
    return render(request, "dashboard/messages_list.html", context)

@login_required
def message_thread(request: HttpRequest, user_id: int) -> HttpResponse:
    """Переписка с конкретным пользователем"""
    other_user = get_object_or_404(User, id=user_id)

    unread = Message.objects.filter(sender=other_user,receiver=request.user,is_read=False)
    unread.update(is_read=True)

    messages_l = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).order_by('timestamp')

    if request.method == "POST":
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(sender=request.user,receiver=other_user,content=content)
            return redirect('message_thread', user_id=user_id)

    context = {
        'other_user': other_user,
        'messages': messages_l,
        'post_user_username': other_user.username
    }
    return render(request, "dashboard/message_thread.html", context)
