function markAsReadAndNavigate(notificationId) {
    // Сразу меняем внешний вид
    const item = document.querySelector(`[data-notification-id="${notificationId}"]`);
    if (item) {
        item.classList.remove('unread');
        const dot = item.querySelector('.unread-dot');
        if (dot) dot.remove();
    }
    
    // Отправляем запрос на сервер
    const formData = new FormData();
    formData.append('notification_id', notificationId);
    
    fetch(`/notifications/${notificationId}/mark-read/`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCSRFToken()
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateUnreadCount();
        }
    })
    .catch(error => console.error('Error:', error));
}

function markAllAsRead() {
    // Сразу меняем внешний вид всех уведомлений
    document.querySelectorAll('.notification-item.unread').forEach(item => {
        item.classList.remove('unread');
        const dot = item.querySelector('.unread-dot');
        if (dot) dot.remove();
    });
    
    // Отправляем запрос на сервер
    fetch(`/mark_all_read/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken()
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateUnreadCount();
        }
    })
    .catch(error => console.error('Error:', error));
}

function updateUnreadCount() {
    const unreadCount = document.querySelectorAll('.notification-item.unread').length;
    const badge = document.querySelector('.unread-badge');
    const markAllBtn = document.querySelector('.btn-primary');
    
    if (unreadCount === 0 && markAllBtn) {
        markAllBtn.remove();
    }
}

// Функция для получения CSRF токена
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
           document.cookie.match(/csrftoken=([^;]+)/)?.[1];
}