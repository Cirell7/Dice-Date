function saveOnboarding() {
    const birthDate = document.getElementById('birth_date').value;
    const submitBtn = document.getElementById('submit-btn');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    if (!birthDate) {
        alert('Пожалуйста, заполните дату рождения');
        return;
    }

    submitBtn.disabled = true;
    submitBtn.textContent = 'Сохранение...';
    
    const formData = new FormData();
    formData.append('birth_date', birthDate);
    
    fetch("", {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrfToken
        },
        redirect: 'manual' // Важно: обрабатываем редиректы вручную
    })
    .then(response => {
        if (response.status === 0 || response.status === 200) {
            // УСПЕХ - редирект на профиль
            window.location.href = onboardingUrls.profile;
        } else if (response.status === 302) {
            // РЕДИРЕКТ - следуем за ним
            return response.text().then(() => {
                window.location.href = onboardingUrls.profile;
            });
        } else {
            // ОШИБКА - показываем сообщение
            return response.json().then(data => {
                if (data.error === 1) {
                    alert('Извините, наш сайт предназначен для пользователей старше 16 лет');
                } else {
                    alert('Произошла ошибка при сохранении');
                }
                submitBtn.disabled = false;
                submitBtn.textContent = 'Продолжить';
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Произошла ошибка при сохранении. Попробуйте еще раз.');
        submitBtn.disabled = false;
        submitBtn.textContent = 'Продолжить';
    });
}