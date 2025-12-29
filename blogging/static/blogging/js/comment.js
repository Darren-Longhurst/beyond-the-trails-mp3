 document.addEventListener('DOMContentLoaded', () => {

 /* Edit Comment Handling */

    document.querySelectorAll('.edit-comment-btn').forEach(button => {
        button.addEventListener('click', () => {
            const commentId = button.dataset.commentId;
            const form = document.getElementById(`edit-comment-form-${commentId}`);
            const textarea = document.getElementById(`edit-comment-textarea-${commentId}`);
            const commentBody = document.getElementById(`comment${commentId}`);
            const cancelButton = form.querySelector('.cancel-edit-btn');

            if (!form || !textarea || !commentBody || !cancelButton) return;

            // Show edit for on button click
                commentBody.style.display = 'none';
                form.style.display = 'block';
                textarea.focus();

            // Cancel button hides the form and restores original comment view
            cancelButton.onclick = () => {
                form.style.display = 'none';
                commentBody.style.display = 'block';
            };
        });
    });


    /* Delete Comment Modal Handling */

    /*Modal cleanup to prevent backdrop issues*/

    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('hidden.bs.modal', () => {
            document.body.classList.remove('modal-open');
            document.querySelectorAll('.modal-backdrop').forEach(backdrop => backdrop.remove());
    });
});

    /* Show delete confirmation modal */

    document.querySelectorAll('.delete-comment-btn').forEach(button => {
        button.addEventListener('click', () => {
            const commentId = button.dataset.commentId;

            const modalElement = document.getElementById(`deleteCommentModal${commentId}`);
            if (!modalElement) return;

            const modal = new bootstrap.Modal(modalElement);
            modal.show();
        });
    });

});

