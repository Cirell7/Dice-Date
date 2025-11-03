// Drag & drop для загрузки фото
document.addEventListener('DOMContentLoaded', function() {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const fileName = document.getElementById('fileName');
    const browseBtn = document.querySelector('.browse-btn');
    const closeBtn = document.querySelector('.modal .close-btn');
    const modal = document.getElementById('uploadModal');

    if (!dropZone || !fileInput) return;

    // Обработчик выбора файла
    fileInput.addEventListener('change', function() {
        if (this.files.length) {
            fileName.textContent = this.files[0].name;
            // АВТОМАТИЧЕСКАЯ ЗАГРУЗКА при выборе файла
            uploadPhoto(this.files[0]);
        }
    });

    // Кнопка "Выберите файл"
    if (browseBtn) {
        browseBtn.addEventListener('click', function() {
            fileInput.click();
        });
    }

    // Закрытие модалки
    if (closeBtn) {
        closeBtn.addEventListener('click', function(e) {
            e.preventDefault();
            closeModal();
        });
    }

    // Drag & drop события
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    // Подсветка при drag over
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => {
            dropZone.classList.add('dragover');
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => {
            dropZone.classList.remove('dragover');
        }, false);
    });

    // Обработка drop
    dropZone.addEventListener('drop', function(e) {
        const files = e.dataTransfer.files;
        if (files.length) {
            fileInput.files = files;
            fileName.textContent = files[0].name;
            // АВТОМАТИЧЕСКАЯ ЗАГРУЗКА при drop
            uploadPhoto(files[0]);
        }
    });

    // Функция автоматической загрузки фото
    function uploadPhoto(file) {
        const form = document.getElementById('uploadForm');
        const formData = new FormData(form); // Автоматически соберет CSRF!
        formData.append('photo', file);
        formData.append('update_photo', 'true');
    
        const fileName = document.getElementById('fileName');
        const browseBtn = document.querySelector('.browse-btn');
    
        fileName.textContent = 'Загрузка...';
        if (browseBtn) browseBtn.disabled = true;
    
        fetch('', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                closeModal();
                window.location.reload();
            } else {
                throw new Error('Ошибка загрузки');
            }
        })
        .catch(error => {
            fileName.textContent = 'Ошибка загрузки';
            alert('Ошибка загрузки фото');
        })
        .finally(() => {
            if (browseBtn) browseBtn.disabled = false;
        });
    }

    // Закрытие модалки по клику вне её
    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === this) {
                closeModal();
            }
        });
    }
});

// Простые функции для модалки
function openUploadModal() {
    document.getElementById('uploadModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('uploadModal').style.display = 'none';
}