function skipOnboarding() {
    document.querySelector('.onboarding-overlay').style.display = 'none';
    window.location.href = "/profile_onboarding2/";
}
function closeOnboarding() {
    document.querySelector('.onboarding-overlay').style.display = 'none';
    window.location.href = "/post_list/";
}
function saveOnboarding() {
    const selectedGender = document.querySelector('input[name="gender"]:checked');
    const submitBtn = document.getElementById('submit-btn');
    
    // ПРАВИЛЬНОЕ получение CSRF токена
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    // Простая валидация
    if (!selectedGender) {
        alert('Пожалуйста, выберите ваш пол');
        return;
    }

    // Блокируем кнопку
    submitBtn.disabled = true;
    submitBtn.textContent = 'Сохранение...';
    
    // Подготавливаем данные
    const formData = new FormData();
    formData.append('gender', selectedGender.value);
    // CSRF токен УЖЕ в форме, не нужно добавлять вручную
    
    // Отправляем данные с правильными заголовками
    fetch("", {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrfToken  // ← ДОБАВЬ ЭТОТ ЗАГОЛОВОК
        }
    })
    .then(response => {
        if (response.ok) {
            window.location.href = "/profile_onboarding2/";
        } else {
            throw new Error('Ошибка сервера');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Произошла ошибка при сохранении. Попробуйте еще раз.');
        submitBtn.disabled = false;
        submitBtn.textContent = 'Продолжить';
    });
}