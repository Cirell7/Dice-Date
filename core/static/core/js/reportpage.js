function openErrorModal() {
    document.getElementById('error-modal').style.display = 'block';
}

function closeErrorModal() {
    document.getElementById('error-modal').style.display = 'none';
}

// Закрытие по клику вне модалки
window.addEventListener('click', function(event) {
    const modal = document.getElementById('error-modal');
    if (event.target === modal) {
        closeErrorModal();
    }
});

// Закрытие по ESC
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeErrorModal();
    }
});