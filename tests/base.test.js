/**
 * @jest-environment jsdom
 */

const { initAlertFade } = require('../static/js/base');

describe('Django Alert Fade', () => {
    beforeEach(() => {
        // 1. Set up our document body
        document.body.innerHTML = `
            <div id="msg1" class="alert show">Message 1</div>
            <div id="msg2" class="alert show">Message 2</div>
        `;

        // 2. Tell Jest to use "fake" timers
        jest.useFakeTimers();
    });

    afterEach(() => {
        jest.clearAllTimers();
    });

    test('should remove "show" class after 6 seconds and remove element after 6.5 seconds', () => {
        initAlertFade();

        const alert = document.querySelector('#msg1');

        // Fast-forward 6 seconds
        jest.advanceTimersByTime(6000);
        expect(alert.classList.contains('show')).toBe(false);

        // Fast-forward another 500ms
        jest.advanceTimersByTime(500);
        expect(document.querySelector('#msg1')).setNull; // Element should be gone
    });
});
