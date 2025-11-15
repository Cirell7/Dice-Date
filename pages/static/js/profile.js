// static/js/profile-editing.js
document.addEventListener('click', function(e) {
    // Если клик по кнопке отмены
    if (e.target.classList.contains('cancel-btn')) {
        const field = e.target.closest('.editable-field');
        if (field) {
            const fieldName = field.dataset.field;
            cancelEditing(fieldName);
            e.stopPropagation();
        }
    }
    
    // Если клик по кнопке сохранения
    if (e.target.classList.contains('save-btn')) {
        const field = e.target.closest('.editable-field');
        if (field) {
            const fieldName = field.dataset.field;
            saveField(fieldName);
            e.stopPropagation();
        }
    }
});

let originalValues = {};
let currentEditingField = null;
function startEditing(fieldName) {
    if (currentEditingField) {
        cancelEditing(currentEditingField);
    }
    
    const field = document.querySelector(`[data-field="${fieldName}"]`);
    if (!field) return;
    
    const valueElement = field.querySelector('.field-value');
    const inputElement = field.querySelector('.edit-input, .edit-textarea, .edit-select');
    const actionsElement = document.getElementById(`${fieldName}-actions`);
    
    if (valueElement) valueElement.style.display = 'none';
    if (inputElement) inputElement.style.display = 'inline-block';
    if (actionsElement) actionsElement.style.display = 'block';
    
    field.classList.add('editing');
    currentEditingField = fieldName;
    
    if (inputElement && (inputElement.tagName === 'INPUT' || inputElement.tagName === 'TEXTAREA')) {
        inputElement.focus();
    }
}

function cancelEditing(fieldName) {
    const field = document.querySelector(`[data-field="${fieldName}"]`);
    if (!field) return;
    
    const valueElement = field.querySelector('.field-value');
    const inputElement = field.querySelector('.edit-input, .edit-textarea, .edit-select');
    const actionsElement = document.getElementById(`${fieldName}-actions`);
    
    // Восстанавливаем оригинальные стили (убираем inline стили)
    if (valueElement) valueElement.style.display = '';
    if (inputElement) inputElement.style.display = 'none'; // оставляем скрытым
    if (actionsElement) actionsElement.style.display = 'none'; // оставляем скрытым
    
    field.classList.remove('editing');
    currentEditingField = null;
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
        if (data.error === 1 && fieldName === 'username') {
            window.location.reload();
        } else {
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
