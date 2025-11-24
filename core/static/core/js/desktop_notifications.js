// notifications.js - Функционал для работы с уведомлениями

class NotificationManager {
    constructor() {
        this.csrfToken = this.getCSRFToken();
        this.init();
    }

    init() {
        this.bindEvents();
        this.updateNotificationBadges();
    }

    // Получение CSRF токена
    getCSRFToken() {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
        return csrfToken ? csrfToken.value : '';
    }

    // Привязка событий
    bindEvents() {
        // Привязываем клики на уведомления
        document.addEventListener('click', (e) => {
            const notificationItem = e.target.closest('.notification-item');
            if (notificationItem) {
                this.handleNotificationClick(notificationItem, e);
            }
        });

        // Закрытие dropdown при клике вне области
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.notification-dropdown') && 
                !e.target.closest('.dropdown-toggle')) {
                this.closeAllDropdowns();
            }
        });
    }

    // Обработка клика на уведомление
    async handleNotificationClick(notificationItem, event) {
        const notificationId = notificationItem.getAttribute('onclick')?.match(/\d+/)?.[0];
        
        if (notificationId) {
            event.preventDefault();
            
            try {
                await this.markAsRead(notificationId);
                this.updateNotificationUI(notificationItem, notificationId);
                this.closeDropdown(notificationItem);
                
                // Переход по ссылке после отметки как прочитано
                const href = notificationItem.getAttribute('href');
                if (href && href !== '#') {
                    setTimeout(() => {
                        window.location.href = href;
                    }, 100);
                }
            } catch (error) {
                console.error('Error marking notification as read:', error);
                // В случае ошибки всё равно переходим по ссылке
                const href = notificationItem.getAttribute('href');
                if (href && href !== '#') {
                    window.location.href = href;
                }
            }
        }
    }

    // Отметить уведомление как прочитанное
    async markAsRead(notificationId) {
        const response = await fetch(`/notifications/${notificationId}/mark-read/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': this.csrfToken,
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error('Failed to mark notification as read');
        }

        return await response.json();
    }

    // Обновление UI после прочтения уведомления
    updateNotificationUI(notificationItem, notificationId) {
        // Убираем класс непрочитанного
        notificationItem.classList.remove('notification-unread');
        
        // Убираем бейдж "Новое"
        const newBadge = notificationItem.querySelector('.badge.bg-primary');
        if (newBadge) {
            newBadge.remove();
        }

        // Обновляем счётчик непрочитанных
        this.updateNotificationCount(-1);
    }

    // Обновление счётчика непрочитанных
    updateNotificationCount(change) {
        const badges = document.querySelectorAll('.notification-badge');
        
        badges.forEach(badge => {
            let currentCount = parseInt(badge.textContent) || 0;
            currentCount += change;
            
            if (currentCount > 0) {
                badge.textContent = currentCount;
                badge.style.display = 'inline-flex';
            } else {
                badge.style.display = 'none';
            }
        });
    }

    // Закрытие конкретного dropdown
    closeDropdown(notificationItem) {
        const dropdown = notificationItem.closest('.dropdown-menu');
        if (dropdown) {
            const dropdownToggle = dropdown.previousElementSibling;
            if (dropdownToggle && bootstrap?.Dropdown) {
                const dropdownInstance = bootstrap.Dropdown.getInstance(dropdownToggle);
                if (dropdownInstance) {
                    dropdownInstance.hide();
                }
            }
        }
    }

    // Закрытие всех dropdown
    closeAllDropdowns() {
        const dropdowns = document.querySelectorAll('.dropdown-menu');
        dropdowns.forEach(dropdown => {
            const dropdownToggle = dropdown.previousElementSibling;
            if (dropdownToggle && bootstrap?.Dropdown) {
                const dropdownInstance = bootstrap.Dropdown.getInstance(dropdownToggle);
                if (dropdownInstance) {
                    dropdownInstance.hide();
                }
            }
        });
    }

    // Обновление бейджей (для реального времени)
    updateNotificationBadges() {
        // Можно добавить периодическое обновление через WebSocket или Polling
        // setInterval(() => this.fetchNotificationCount(), 30000);
    }

    // Запрос актуального количества уведомлений
    async fetchNotificationCount() {
        try {
            const response = await fetch('/notifications/api/unread-count/');
            if (response.ok) {
                const data = await response.json();
                this.updateBadgeDisplay(data.unread_count);
            }
        } catch (error) {
            console.error('Error fetching notification count:', error);
        }
    }

    // Обновление отображения бейджа
    updateBadgeDisplay(count) {
        const badges = document.querySelectorAll('.notification-badge');
        
        badges.forEach(badge => {
            if (count > 0) {
                badge.textContent = count;
                badge.style.display = 'inline-flex';
            } else {
                badge.style.display = 'none';
            }
        });
    }

    // Пометить все как прочитанные
    async markAllAsRead() {
        try {
            const response = await fetch('/notifications/mark-all-read/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.csrfToken,
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                this.updateBadgeDisplay(0);
                
                // Убираем все отметки "Новое"
                document.querySelectorAll('.notification-unread').forEach(item => {
                    item.classList.remove('notification-unread');
                });
                
                document.querySelectorAll('.badge.bg-primary').forEach(badge => {
                    badge.remove();
                });
                
                return true;
            }
        } catch (error) {
            console.error('Error marking all notifications as read:', error);
        }
        return false;
    }
}

// Утилитарные функции
const NotificationUtils = {
    // Форматирование времени
    formatTime(timestamp) {
        const now = new Date();
        const notificationTime = new Date(timestamp);
        const diffMs = now - notificationTime;
        const diffMins = Math.floor(diffMs / 60000);
        const diffHours = Math.floor(diffMs / 3600000);
        const diffDays = Math.floor(diffMs / 86400000);

        if (diffMins < 1) return 'только что';
        if (diffMins < 60) return `${diffMins} мин назад`;
        if (diffHours < 24) return `${diffHours} ч назад`;
        if (diffDays < 7) return `${diffDays} дн назад`;
        
        return notificationTime.toLocaleDateString('ru-RU');
    },

    // Эффект вибрации для новых уведомлений
    vibrate() {
        if ('vibrate' in navigator) {
            navigator.vibrate(100);
        }
    },

    // Показать toast-уведомление
    showToast(message, type = 'info') {
        // Реализация toast-уведомлений, если нужно
        console.log(`[${type}] ${message}`);
    }
};

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    window.notificationManager = new NotificationManager();
});

// Экспорт для использования в других модулях
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { NotificationManager, NotificationUtils };
}