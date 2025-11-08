let checkTimeout;

document.addEventListener('DOMContentLoaded', function() {
    const usernameInput = document.querySelector('input[name="username"]');
    const statusElement = document.getElementById('username-status');
    
    if (usernameInput && statusElement) {
        usernameInput.addEventListener('input', function() {
            const username = this.value.trim();

            clearTimeout(checkTimeout);

            if (username.length < 3) {
                statusElement.textContent = '✗ Минимум 3 символа';
                statusElement.className = 'username-status taken';
                return;
            }
            
            // Для валидной длины проверяем уникальность через ТВОЙ API
            checkTimeout = setTimeout(() => {
                fetch(`/api/check-username/?username=${encodeURIComponent(username)}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.available) {
                            statusElement.textContent = '✓ Доступно';
                            statusElement.className = 'username-status available';
                        } else {
                            statusElement.textContent = '✗ Занято';
                            statusElement.className = 'username-status taken';
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        statusElement.textContent = '⚠️ Ошибка проверки';
                    });
            }, 500);
        });
    }
});