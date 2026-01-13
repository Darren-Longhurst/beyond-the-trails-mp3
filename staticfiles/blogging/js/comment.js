/* Logic for toggling the edit form */
function initializeEditButtons() {
    document.querySelectorAll('.edit-comment-btn').forEach(button => {
        button.addEventListener('click', () => {
            const commentId = button.dataset.commentId;
            const form = document.getElementById(`edit-comment-form-${commentId}`);
            const textarea = document.getElementById(`edit-comment-textarea-${commentId}`);
            const commentBody = document.getElementById(`comment${commentId}`);
            const cancelButton = form?.querySelector('.cancel-edit-btn');

            if (!form || !textarea || !commentBody || !cancelButton) return;

            commentBody.style.display = 'none';
            form.style.display = 'block';
            textarea.focus();

            cancelButton.onclick = () => {
                form.style.display = 'none';
                commentBody.style.display = 'block';
            };
        });
    });
}

/* Logic for Modal Cleanup */
function initializeModalCleanup() {
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('hidden.bs.modal', () => {
            document.body.classList.remove('modal-open');
            document.querySelectorAll('.modal-backdrop').forEach(backdrop => backdrop.remove());
        });
    });
}

// Run functions when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    initializeEditButtons();
    initializeModalCleanup();
    // ... add your delete logic here too ...
});

// Export for Jest
if (typeof module !== 'undefined') {
    module.exports = { initializeEditButtons, initializeModalCleanup };
}
