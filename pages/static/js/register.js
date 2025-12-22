document.addEventListener('DOMContentLoaded', () => {
    const input = document.querySelector('input[name="username"]');
    const status = document.getElementById('username-status');
    let timeout;
    
    input?.addEventListener('input', ({target}) => {
        const username = target.value.trim();
        clearTimeout(timeout);
        
        if (username.length < 3) {
            status.textContent = '✗ Минимум 3 символа';
            return
        }
        
        timeout = setTimeout(() => {
            fetch('/api/check-username/?username=' + username)
                .then(response  => response.json())
                .then(({available}) => {
                    status.textContent = available ? '✓ Доступно' : '✗ Занято';
                })
                .catch(() => status.textContent = '⚠️ Ошибка проверки');
        }, 500);
    });
});