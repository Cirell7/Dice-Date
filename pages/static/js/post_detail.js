document.addEventListener('DOMContentLoaded', function() {
    // Обработка удаления комментариев
    document.querySelectorAll('.delete-comment').forEach(button => {
        button.addEventListener('click', function() {
            const commentId = this.getAttribute('data-comment-id');
            const postId = this.getAttribute('data-post-id');
            
            if (confirm('Вы уверены, что хотите удалить этот комментарий?')) {
                deleteComment(commentId, postId, this);
            }
        });
    });
    
    function deleteComment(commentId, postId, buttonElement) {
        const csrfToken = document.getElementById('csrf-token').dataset.csrf;
        const formData = new FormData();
        formData.append('action', 'delete_comment');
        formData.append('comment_id', commentId);
    
        fetch(window.location.href, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const commentItem = buttonElement.closest('.comment-item');
                commentItem.remove();
            } else {
                alert('Ошибка при удалении комментария: ' + data.error);
            }
        })
        .catch(error => {
            alert('Комментарий удален, перезагрузите страницу');
        });
    }
});