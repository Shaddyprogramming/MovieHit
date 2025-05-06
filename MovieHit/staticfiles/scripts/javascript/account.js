/**
 * MovieHit Account Management JavaScript
 * Handles account section navigation, email updates, and password resets
 */
document.addEventListener('DOMContentLoaded', function () {
    // Tab switching functionality for account sections
    initializeTabNavigation();

    // Initialize security features
    initializeEmailUpdate();
    initializePasswordReset();

    // Initialize preference toggles
    initializePreferenceToggles();
});

/**
 * Sets up tab navigation between account sections
 */
function initializeTabNavigation() {
    const menuItems = document.querySelectorAll('.sidebar-item');
    const contentSections = document.querySelectorAll('.content-section');

    menuItems.forEach(item => {
        item.addEventListener('click', function (e) {
            e.preventDefault();
            const target = this.getAttribute('href').substring(1);

            // Update active state in menu
            menuItems.forEach(i => i.classList.remove('active'));
            this.classList.add('active');

            // Show selected content section
            contentSections.forEach(section => {
                section.classList.remove('active');
                if (section.id === target) {
                    section.classList.add('active');
                }
            });
        });
    });
}

/**
 * Sets up email update functionality
 */
function initializeEmailUpdate() {
    const updateEmailBtn = document.getElementById('update-email-btn');
    const emailMessage = document.getElementById('email-message');

    if (!updateEmailBtn || !emailMessage) return;

    updateEmailBtn.addEventListener('click', function () {
        // Show loading state
        updateEmailBtn.disabled = true;
        updateEmailBtn.textContent = 'Sending...';
        showMessage(emailMessage, 'Processing your request...', 'info');

        // Get CSRF token for secure request
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        // Send request to initiate email change process
        fetch('/update_email/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
            .then(handleResponse)
            .then(data => {
                // Reset button state
                updateEmailBtn.disabled = false;
                updateEmailBtn.textContent = 'Change Email';

                if (data.success) {
                    showMessage(emailMessage, 'Check your current email for a link to update your email address.', 'success');
                } else {
                    showMessage(emailMessage, data.error || 'Failed to send email update link.', 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                updateEmailBtn.disabled = false;
                updateEmailBtn.textContent = 'Change Email';
                showMessage(emailMessage, 'An error occurred. Please try again.', 'error');
            });
    });
}

/**
 * Sets up password reset functionality
 */
function initializePasswordReset() {
    const resetPasswordBtn = document.getElementById('reset-password-btn');
    const passwordMessage = document.getElementById('password-message');

    if (!resetPasswordBtn || !passwordMessage) return;

    resetPasswordBtn.addEventListener('click', function () {
        const userEmail = document.querySelector('input[name="email"]').value;

        if (!userEmail) {
            showMessage(passwordMessage, 'You need an email address set for your account to reset password.', 'error');
            return;
        }

        // Show loading state
        resetPasswordBtn.disabled = true;
        resetPasswordBtn.textContent = 'Sending...';
        showMessage(passwordMessage, 'Processing your request...', 'info');

        // Get CSRF token for secure request
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        // Send password reset request
        fetch('/password_reset/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: `email=${encodeURIComponent(userEmail)}&direct_reset=true`
        })
            .then(handleResponse)
            .then(data => {
                // Reset button state
                resetPasswordBtn.disabled = false;
                resetPasswordBtn.textContent = 'Reset Password';

                if (data.success) {
                    showMessage(passwordMessage, 'Check your email for a link to reset your password.', 'success');
                } else {
                    showMessage(passwordMessage, data.error || 'Failed to send reset link.', 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                resetPasswordBtn.disabled = false;
                resetPasswordBtn.textContent = 'Reset Password';
                showMessage(passwordMessage, 'An error occurred. Please try again.', 'error');
            });
    });
}

/**
 * Sets up preference toggles functionality
 */
function initializePreferenceToggles() {
    const toggles = document.querySelectorAll('.toggle-switch input');

    toggles.forEach(toggle => {
        toggle.addEventListener('change', function () {
            // Get the preference label and checked state
            const label = this.parentElement.nextElementSibling.textContent;
            const isChecked = this.checked;

            // Future implementation: Save preference to user settings via AJAX
            console.log(`Preference "${label}" set to: ${isChecked}`);

            // Here you would typically save this preference via AJAX
            // For now we just log it to console
        });
    });
}

/**
 * Handles API response and provides error handling
 * @param {Response} response - Fetch API response object
 * @returns {Promise} - JSON data or error
 */
function handleResponse(response) {
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json();
}

/**
 * Displays a message with appropriate styling
 * @param {HTMLElement} element - The message container element
 * @param {string} text - Message text to display
 * @param {string} type - Message type (success, error, info)
 */
function showMessage(element, text, type = 'info') {
    if (!element) return;

    // Reset previous styling
    element.classList.remove('hidden', 'success', 'error', 'info');

    // Set message content and type
    element.textContent = text;
    element.classList.add(type);
}
