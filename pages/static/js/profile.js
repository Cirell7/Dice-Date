// static/js/profile-editing.js

let originalValues = {};
let currentEditingField = null;

function startEditing(fieldName) {
    // Если уже редактируем другое поле, сначала сохраняем/отменяем его
    if (currentEditingField && currentEditingField !== fieldName) {
        cancelEditing(currentEditingField);
    }
    
    const field = document.querySelector(`[data-field="${fieldName}"]`);
    const valueElement = field.querySelector('.field-value');
    const inputElement = field.querySelector('.edit-input, .edit-textarea, .edit-select');
    const actionsElement = document.getElementById(`${fieldName}-actions`);
    
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
    if (inputElement.tagName === 'SELECT') {
        const options = inputElement.options;
        for (let i = 0; i < options.length; i++) {
            if (options[i].value === originalValues[fieldName]) {
                inputElement.selectedIndex = i;
                break;
            }
        }
    } else {
        inputElement.value = originalValues[fieldName];
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
}
function saveField(fieldName) {
    const field = document.querySelector(`[data-field="${fieldName}"]`);
    const inputElement = field.querySelector('.edit-input, .edit-textarea, .edit-select');
    const valueElement = field.querySelector('.field-value');
    const actionsElement = document.getElementById(`${fieldName}-actions`);
    
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
    
    console.log(`DEBUG: Saving field ${fieldName} with value: ${formData.get(fieldName)}`);  // ← ДОБАВЬТЕ
    
    fetch('', {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log('DEBUG: Server response:', data);  // ← ДОБАВЬТЕ
        if (data.error === 1 && fieldName === 'username') {
            console.log('DEBUG: Username error detected, reloading...');  // ← ДОБАВЬТЕ
            window.location.reload();
        } else {
            console.log('DEBUG: Success, reloading...');  // ← ДОБАВЬТЕ
            window.location.reload();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        window.location.reload();
    });
}

// Простые функции для модалки - ОДНА ВЕРСИЯ!
function openUploadModal() {
    document.getElementById('uploadModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('uploadModal').style.display = 'none';
}

// ДЕЛАЕМ ФУНКЦИИ ГЛОБАЛЬНЫМИ для доступа из HTML!
window.startEditing = startEditing;
window.cancelEditing = cancelEditing;
window.saveField = saveField;
window.openUploadModal = openUploadModal;
window.closeModal = closeModal;
