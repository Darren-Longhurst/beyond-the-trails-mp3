/**
 * @jest-environment jsdom
 */

const { initializeEditButtons } = require('../blogging/static/blogging/js/comment');

describe('Comment Edit Toggle', () => {
    beforeEach(() => {
        // Set up the specific HTML structure your JS expects
        document.body.innerHTML = `
            <div id="comment10" style="display: block;">Original Content</div>
            <form id="edit-comment-form-10" style="display: none;">
                <textarea id="edit-comment-textarea-10"></textarea>
                <button type="button" class="cancel-edit-btn">Cancel</button>
            </form>
            <button class="edit-comment-btn" data-comment-id="10">Edit</button>
        `;
        // Initialize the listeners
        initializeEditButtons();
    });

    test('clicking edit button should hide comment and show form', () => {
        const editBtn = document.querySelector('.edit-comment-btn');
        const commentBody = document.getElementById('comment10');
        const form = document.getElementById('edit-comment-form-10');

        editBtn.click();

        expect(commentBody.style.display).toBe('none');
        expect(form.style.display).toBe('block');
    });

    test('clicking cancel should restore original view', () => {
        const editBtn = document.querySelector('.edit-comment-btn');
        const cancelBtn = document.querySelector('.cancel-edit-btn');
        const commentBody = document.getElementById('comment10');
        const form = document.getElementById('edit-comment-form-10');

        editBtn.click(); // Open it first
        cancelBtn.click(); // Then cancel

        expect(form.style.display).toBe('none');
        expect(commentBody.style.display).toBe('block');
    });
});
