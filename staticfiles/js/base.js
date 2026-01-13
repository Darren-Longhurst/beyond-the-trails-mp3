/* Django message timeout fade*/
const initAlertFade = () => {
    document.querySelectorAll('.alert').forEach(alert => {
        setTimeout(() => {
            alert.classList.remove('show');
            setTimeout(() => {
                alert.remove();
            }, 500);
        }, 6000);
    });
};

// Run it on load
document.addEventListener('DOMContentLoaded', initAlertFade);

// Export for Jest
if (typeof module !== 'undefined') {
    module.exports = { initAlertFade };
}
