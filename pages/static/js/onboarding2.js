function closeOnboarding() {
    document.querySelector('.onboarding-overlay').style.display = 'none';
    window.location.href = onboardingUrls.profile;
}

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
        }
    })
    .then(response => response.json())  // ← ЧИТАЕМ JSON!
    .then(data => {
        if (data.error === 0) {
            // УСПЕХ (error=0) - переходим в профиль
            window.location.href = onboardingUrls.profile;
        } else {
            // ОШИБКА (error=1) - НЕ переходим, показываем сообщение
            alert('Извините, наш сайт предназначен для пользователей старше 16 лет');
            submitBtn.disabled = false;
            submitBtn.textContent = 'Продолжить';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Произошла ошибка при сохранении. Попробуйте еще раз.');
        submitBtn.disabled = false;
        submitBtn.textContent = 'Продолжить';
    });
}