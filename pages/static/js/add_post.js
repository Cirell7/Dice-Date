// Ждем полной загрузки DOM
document.addEventListener('DOMContentLoaded', function() {
    // Показ имени файла при выборе
    const imageInput = document.getElementById('image');
    if (imageInput) {
        imageInput.addEventListener('change', function(e) {
            const fileName = document.getElementById('file-name');
            if (this.files[0]) {
                fileName.textContent = this.files[0].name;
            } else {
                fileName.textContent = '';
            }
        });
    }

    // Drag and drop для файла
    const fileUpload = document.querySelector('.file-upload-area');
    if (fileUpload) {
        fileUpload.addEventListener('dragover', function(e) {
            e.preventDefault();
            this.classList.add('dragover');
        });

        fileUpload.addEventListener('dragleave', function() {
            this.classList.remove('dragover');
        });

        fileUpload.addEventListener('drop', function(e) {
            e.preventDefault();
            this.classList.remove('dragover');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                document.getElementById('image').files = files;
                document.getElementById('file-name').textContent = files[0].name;
            }
        });
    }

    // Установка минимальной даты (текущее время)
    const dateInput = document.getElementById('event_date');
    if (dateInput) {
        const now = new Date();
        now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
        dateInput.min = now.toISOString().slice(0, 16);
    }
});