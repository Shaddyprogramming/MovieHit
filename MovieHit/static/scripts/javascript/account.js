/**
 * MovieHit Account Management JavaScript
 * Handles account section navigation, email updates, password resets,
 * and user preferences
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

            // Update URL hash without scrolling
            history.replaceState(null, null, `#${target}`);
        });
    });

    // Check if there's a hash in the URL to activate that tab
    if (window.location.hash) {
        const targetId = window.location.hash.substring(1);
        const targetMenu = document.querySelector(`.sidebar-item[href="#${targetId}"]`);
        if (targetMenu) {
            targetMenu.click();
        }
    }
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
        // Load saved preferences from localStorage
        const preferenceName = toggle.parentElement.nextElementSibling.textContent.trim();
        if (preferenceName === "Auto-play trailers") {
            toggle.checked = localStorage.getItem('autoplayTrailers') === 'true';
        } else if (preferenceName === "Order sensitive search") {
            toggle.checked = localStorage.getItem('orderSensitiveSearch') === 'true';
        }

        // Set up change event handler
        toggle.addEventListener('change', function () {
            // Get the preference label and checked state
            const label = this.parentElement.nextElementSibling.textContent.trim();
            const isChecked = this.checked;

            // Handle different preference types
            if (label === "Auto-play trailers") {
                saveAutoplayPreference(isChecked);
            } else if (label === "Order sensitive search") {
                saveOrderSensitivePreference(isChecked);
            }

            // Show visual feedback
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
    // Check if we have an endpoint to save preferences
    try {
        // Get CSRF token for secure request
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        // If no CSRF token, we might be working with just localStorage
        if (!csrfToken) return;

        // Use cookies as a fallback mechanism
        document.cookie = `${name}=${value}; path=/; max-age=${365 * 24 * 60 * 60}; SameSite=Lax`;

        // Attempt to save to server if save_preference endpoint exists
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
                // This might happen if the endpoint doesn't exist, which is fine
                // We already saved to localStorage and cookie
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
    // Create confirmation element
    const feedbackEl = document.createElement('span');
    feedbackEl.className = 'preference-saved';
    feedbackEl.textContent = '✓ Saved';

    // Style the element
    feedbackEl.style.marginLeft = '10px';
    feedbackEl.style.color = '#4CAF50';
    feedbackEl.style.fontWeight = 'bold';
    feedbackEl.style.opacity = '1';
    feedbackEl.style.transition = 'opacity 0.5s ease-out';

    // Remove any existing feedback
    const existingFeedback = parentElement.querySelector('.preference-saved');
    if (existingFeedback) {
        existingFeedback.remove();
    }

    // Add new feedback
    parentElement.appendChild(feedbackEl);

    // Remove feedback after a delay
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

    // Reset previous styling
    element.classList.remove('hidden', 'success', 'error', 'info');

    // Set message content and type
    element.textContent = text;
    element.classList.add(type);

    // Ensure element is visible with smooth scrolling
    element.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}
