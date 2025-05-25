document.addEventListener('DOMContentLoaded', function () {
    initializeTabNavigation();

    initializeEmailUpdate();
    initializePasswordReset();

    initializePreferenceToggles();
});

function initializeTabNavigation() {
    const menuItems = document.querySelectorAll('.sidebar-item');
    const contentSections = document.querySelectorAll('.content-section');

    menuItems.forEach(item => {
        item.addEventListener('click', function (e) {
            e.preventDefault();
            const target = this.getAttribute('href').substring(1);

            menuItems.forEach(i => i.classList.remove('active'));
            this.classList.add('active');

            contentSections.forEach(section => {
                section.classList.remove('active');
                if (section.id === target) {
                    section.classList.add('active');
                }
            });

            history.replaceState(null, null, `#${target}`);
        });
    });

    if (window.location.hash) {
        const targetId = window.location.hash.substring(1);
        const targetMenu = document.querySelector(`.sidebar-item[href="#${targetId}"]`);
        if (targetMenu) {
            targetMenu.click();
        }
    }
}

function initializeEmailUpdate() {
    const updateEmailBtn = document.getElementById('update-email-btn');
    const emailMessage = document.getElementById('email-message');

    if (!updateEmailBtn || !emailMessage) return;

    updateEmailBtn.addEventListener('click', function () {
        updateEmailBtn.disabled = true;
        updateEmailBtn.textContent = 'Sending...';
        showMessage(emailMessage, 'Processing your request...', 'info');

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

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

        resetPasswordBtn.disabled = true;
        resetPasswordBtn.textContent = 'Sending...';
        showMessage(passwordMessage, 'Processing your request...', 'info');

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

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

function initializePreferenceToggles() {
    const toggles = document.querySelectorAll('.toggle-switch input');

    toggles.forEach(toggle => {
        const preferenceName = toggle.parentElement.nextElementSibling.textContent.trim();
        if (preferenceName === "Auto-play trailers") {
            toggle.checked = localStorage.getItem('autoplayTrailers') === 'true';
        } else if (preferenceName === "Order sensitive search") {
            toggle.checked = localStorage.getItem('orderSensitiveSearch') === 'true';
        }

        toggle.addEventListener('change', function () {
            const label = this.parentElement.nextElementSibling.textContent.trim();
            const isChecked = this.checked;

            if (label === "Auto-play trailers") {
                saveAutoplayPreference(isChecked);
            } else if (label === "Order sensitive search") {
                saveOrderSensitivePreference(isChecked);
            }

            showSavedConfirmation(this.parentElement.parentElement);
        });
    });
}

/**
 * Saves autoplay trailer preference to localStorage
 * @param {boolean} isEnabled - Whether autoplay is enabled
 */
function saveAutoplayPreference(isEnabled) {
    localStorage.setItem('autoplayTrailers', isEnabled);
    console.log(`Trailer autoplay set to: ${isEnabled}`);
}

/**
 * Saves order sensitive search preference to localStorage and server
 * @param {boolean} isEnabled - Whether order sensitive search is enabled
 */
function saveOrderSensitivePreference(isEnabled) {
    // Save to localStorage for client-side use
    localStorage.setItem('orderSensitiveSearch', isEnabled);
    console.log(`Order sensitive search set to: ${isEnabled}`);

    // Also save to server so the view function can access it
    savePreferenceToServer('orderSensitiveSearch', isEnabled);
}

/**
 * Sends preference to the server if available via AJAX
 * @param {string} name - Name of the preference
 * @param {boolean} value - Value of the preference
 */
function savePreferenceToServer(name, value) {
    try {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        if (!csrfToken) return;

        document.cookie = `${name}=${value}; path=/; max-age=${365 * 24 * 60 * 60}; SameSite=Lax`;

        fetch('/save_preference/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: `preference_name=${encodeURIComponent(name)}&preference_value=${encodeURIComponent(value)}`
        })
            .then(response => {
                if (!response.ok) {
                    console.log('Preference saved to cookie only (server endpoint might not exist)');
                    return;
                }
                return response.json();
            })
            .then(data => {
                if (data && !data.success) {
                    console.error('Error saving preference to server:', data.error);
                } else if (data && data.success) {
                    console.log('Preference saved to server successfully');
                }
            })
            .catch(error => {
                console.log('Preference saved locally only');
            });
    } catch (error) {
        console.log('Using local storage only for preferences');
    }
}

/**
 * Shows a saved confirmation indicator
 * @param {HTMLElement} parentElement - The parent element to append the indicator to
 */
function showSavedConfirmation(parentElement) {
    const feedbackEl = document.createElement('span');
    feedbackEl.className = 'preference-saved';
    feedbackEl.textContent = '✓ Saved';

    feedbackEl.style.marginLeft = '10px';
    feedbackEl.style.color = '#4CAF50';
    feedbackEl.style.fontWeight = 'bold';
    feedbackEl.style.opacity = '1';
    feedbackEl.style.transition = 'opacity 0.5s ease-out';

    const existingFeedback = parentElement.querySelector('.preference-saved');
    if (existingFeedback) {
        existingFeedback.remove();
    }

    parentElement.appendChild(feedbackEl);

    setTimeout(() => {
        feedbackEl.style.opacity = '0';
        setTimeout(() => {
            if (feedbackEl.parentNode) {
                feedbackEl.parentNode.removeChild(feedbackEl);
            }
        }, 500);
    }, 1500);
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

    element.classList.remove('hidden', 'success', 'error', 'info');

    element.textContent = text;
    element.classList.add(type);

    element.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}
