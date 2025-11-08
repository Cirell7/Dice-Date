function closeErrorModal() {
    document.getElementById('error-modal').style.display = 'none';
}

window.addEventListener('click', function(event) {
    const modal = document.getElementById('error-modal');
    if (event.target === modal) {
        closeErrorModal();
    }
});