// static/js/profile-editing.js

let originalValues = {};
let currentEditingField = null;

function startEditing(fieldName) {
    // Если уже редактируем другое поле, сначала сохраняем/отменяем его
    if (currentEditingField && currentEditingField !== fieldName) {
        cancelEditing(currentEditingField);
    }
    
    const field = document.querySelector(`[data-field="${fieldName}"]`);
    if (!field) {
        console.error('Field not found:', fieldName);
        return;
    }
    
    const valueElement = field.querySelector('.field-value');
    const inputElement = field.querySelector('.edit-input, .edit-textarea, .edit-select');
    const actionsElement = document.getElementById(`${fieldName}-actions`);
    
    if (!valueElement || !inputElement || !actionsElement) {
        console.error('Editing elements not found for field:', fieldName);
        return;
    }
    
    // Сохраняем оригинальное значение
    originalValues[fieldName] = inputElement.value || valueElement.textContent.trim();
    
    // Переходим в режим редактирования
    valueElement.style.display = 'none';
    inputElement.style.display = 'block';
    actionsElement.classList.add('visible');
    field.classList.add('editing');
    
    // Устанавливаем текущее редактируемое поле
    currentEditingField = fieldName;
    
    // Фокусируемся на поле ввода
    if (inputElement.tagName !== 'SELECT') {
        inputElement.focus();
        if (inputElement.tagName === 'TEXTAREA') {
            inputElement.setSelectionRange(inputElement.value.length, inputElement.value.length);
        }
    }
}

function cancelEditing(fieldName) {
    // Если передали null, используем текущее поле
    if (fieldName === null && currentEditingField) {
        fieldName = currentEditingField;
    }
    
    if (!fieldName) return;
    
    const field = document.querySelector(`[data-field="${fieldName}"]`);
    if (!field) return;
    
    const valueElement = field.querySelector('.field-value');
    const inputElement = field.querySelector('.edit-input, .edit-textarea, .edit-select');
    const actionsElement = document.getElementById(`${fieldName}-actions`);
    
    if (!valueElement || !inputElement || !actionsElement) return;
    
    // Восстанавливаем оригинальное значение
    if (originalValues[fieldName] !== undefined) {
        if (inputElement.tagName === 'SELECT') {
            inputElement.value = originalValues[fieldName];
        } else {
            inputElement.value = originalValues[fieldName];
        }
    }
    
    // Выходим из режима редактирования
    valueElement.style.display = 'inline';
    inputElement.style.display = 'none';
    actionsElement.classList.remove('visible');
    field.classList.remove('editing');
    
    // Сбрасываем текущее редактируемое поле
    if (currentEditingField === fieldName) {
        currentEditingField = null;
    }
    
    // Удаляем из сохраненных значений
    delete originalValues[fieldName];
}

function saveField(fieldName) {
    const field = document.querySelector(`[data-field="${fieldName}"]`);
    if (!field) return;
    
    const inputElement = field.querySelector('.edit-input, .edit-textarea, .edit-select');
    const valueElement = field.querySelector('.field-value');
    const actionsElement = document.getElementById(`${fieldName}-actions`);
    
    if (!inputElement || !valueElement || !actionsElement) return;
    
    let displayValue = '';
    
    // Форматируем значение для отображения
    if (fieldName === 'gender') {
        const selectedOption = inputElement.options[inputElement.selectedIndex];
        displayValue = selectedOption.text || 'Не указан';
    } else if (fieldName === 'birth_date') {
        const date = new Date(inputElement.value);
        displayValue = inputElement.value ? date.toLocaleDateString('ru-RU') : 'Не указана';
    } else {
        displayValue = inputElement.value || (fieldName === 'description' ? 'Нет описания' : 'Не указано');
    }
    
    // Обновляем отображаемое значение
    valueElement.textContent = displayValue;
    valueElement.className = 'field-value' + (!inputElement.value ? ' empty-field' : '');
    
    // Выходим из режима редактирования
    valueElement.style.display = 'inline';
    inputElement.style.display = 'none';
    actionsElement.classList.remove('visible');
    field.classList.remove('editing');
    
    // Сбрасываем текущее редактируемое поле
    currentEditingField = null;
    
    // Отправляем данные на сервер
    const formData = new FormData(document.getElementById('profileForm'));
    formData.append('update_field', fieldName);
    
    fetch('', {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (!data.success) {
            console.error('Error updating field');
            // В случае ошибки восстанавливаем старое значение
            cancelEditing(fieldName);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        cancelEditing(fieldName);
    });
}

function openUploadModal() {
    const modal = document.getElementById('uploadModal');
    if (modal) {
        modal.style.display = 'block';
    }
}

function closeModal() {
    const modal = document.getElementById('uploadModal');
    if (modal) {
        modal.style.display = 'none';
    }
}

// Делаем функции глобальными для доступа из HTML
window.startEditing = startEditing;
window.cancelEditing = cancelEditing;
window.saveField = saveField;
window.openUploadModal = openUploadModal;
window.closeModal = closeModal;

// Обработчик кликов вне редактируемого поля
document.addEventListener('click', function(e) {
    if (currentEditingField && !e.target.closest('.editable-field.editing')) {
        cancelEditing(currentEditingField);
    }
});