/**
 * MovieHit Edit Profile JavaScript
 * Handles form validation and submission for profile editing
 */
document.addEventListener('DOMContentLoaded', function () {
    initializeFormValidation();
    handleFormSubmission();
    setupInputEffects();
});

/**
 * Set up form field validation
 */
function initializeFormValidation() {
    const usernameInput = document.getElementById('username');
    const firstNameInput = document.getElementById('first_name');
    const lastNameInput = document.getElementById('last_name');

    // Username validation
    if (usernameInput) {
        usernameInput.addEventListener('blur', function () {
            validateUsername(this);
        });

        usernameInput.addEventListener('input', function () {
            // Clear error styling on input
            this.classList.remove('is-invalid');

            // Update the character counter if it exists
            updateCharacterCounter(this, 'Username', 30);
        });
    }

    // First name validation
    if (firstNameInput) {
        firstNameInput.addEventListener('blur', function () {
            validateNotEmpty(this, 'First name');
        });

        firstNameInput.addEventListener('input', function () {
            this.classList.remove('is-invalid');
        });
    }

    // Last name validation
    if (lastNameInput) {
        lastNameInput.addEventListener('blur', function () {
            validateNotEmpty(this, 'Last name');
        });

        lastNameInput.addEventListener('input', function () {
            this.classList.remove('is-invalid');
        });
    }
}

/**
 * Validate username field
 * @param {HTMLInputElement} input - The username input element
 * @returns {boolean} - Whether the username is valid
 */
function validateUsername(input) {
    const value = input.value.trim();
    const hint = input.parentElement.querySelector('.form-hint');
    const originalHint = "Your unique username on MovieHit";

    if (value.length < 3) {
        input.classList.add('is-invalid');
        if (hint) hint.textContent = "Username must be at least 3 characters";
        return false;
    }

    if (!/^[a-zA-Z0-9_]+$/.test(value)) {
        input.classList.add('is-invalid');
        if (hint) hint.textContent = "Username can only contain letters, numbers, and underscores";
        return false;
    }

    input.classList.remove('is-invalid');
    if (hint) hint.textContent = originalHint;
    return true;
}

/**
 * Validate non-empty field
 * @param {HTMLInputElement} input - The input element to validate
 * @param {string} fieldName - Name of the field for error message
 * @returns {boolean} - Whether the field is valid
 */
function validateNotEmpty(input, fieldName) {
    const value = input.value.trim();

    if (value.length === 0) {
        input.classList.add('is-invalid');
        return false;
    }

    input.classList.remove('is-invalid');
    return true;
}

/**
 * Update character counter for input fields
 * @param {HTMLInputElement} input - The input element
 * @param {string} fieldName - Name of the field
 * @param {number} maxLength - Maximum allowed characters
 */
function updateCharacterCounter(input, fieldName, maxLength) {
    let counter = input.parentElement.querySelector('.character-counter');

    // Create counter if it doesn't exist
    if (!counter) {
        counter = document.createElement('small');
        counter.className = 'character-counter';
        input.parentElement.appendChild(counter);
    }

    const currentLength = input.value.length;
    counter.textContent = `${currentLength}/${maxLength} characters`;

    // Visual warning if over limit
    if (currentLength > maxLength) {
        counter.classList.add('over-limit');
    } else {
        counter.classList.remove('over-limit');
    }
}

/**
 * Handle form submission with validation
 */
function handleFormSubmission() {
    const form = document.querySelector('form');

    if (form) {
        form.addEventListener('submit', function (e) {
            const usernameInput = document.getElementById('username');
            const firstNameInput = document.getElementById('first_name');
            const lastNameInput = document.getElementById('last_name');

            let isValid = true;

            // Validate all fields
            if (usernameInput && !validateUsername(usernameInput)) {
                isValid = false;
            }

            if (firstNameInput && !validateNotEmpty(firstNameInput, 'First name')) {
                isValid = false;
            }

            if (lastNameInput && !validateNotEmpty(lastNameInput, 'Last name')) {
                isValid = false;
            }

            // Prevent submission if validation fails
            if (!isValid) {
                e.preventDefault();

                // Show error message
                let messageBox = document.querySelector('.message-box');
                if (!messageBox) {
                    messageBox = document.createElement('div');
                    messageBox.className = 'message-box error';
                    const formHeader = document.querySelector('.form-header');
                    formHeader.appendChild(messageBox);
                }

                messageBox.textContent = 'Please correct the highlighted fields';
                messageBox.className = 'message-box error';

                // Scroll to error message
                messageBox.scrollIntoView({ behavior: 'smooth', block: 'center' });
            } else {
                // Add loading state to button
                const submitBtn = form.querySelector('button[type="submit"]');
                if (submitBtn) {
                    submitBtn.disabled = true;
                    submitBtn.innerHTML = '<span class="spinner"></span> Saving...';
                }
            }
        });
    }
}

/**
 * Set up visual effects for form inputs
 */
function setupInputEffects() {
    const inputs = document.querySelectorAll('.form-control');

    inputs.forEach(input => {
        // Add focus styles
        input.addEventListener('focus', function () {
            this.parentElement.classList.add('input-focused');
        });

        input.addEventListener('blur', function () {
            this.parentElement.classList.remove('input-focused');
        });

        // Highlight row on focus
        input.addEventListener('focus', function () {
            const row = this.closest('.form-row');
            if (row) row.classList.add('row-active');
        });

        input.addEventListener('blur', function () {
            const row = this.closest('.form-row');
            if (row) row.classList.remove('row-active');
        });
    });
}
