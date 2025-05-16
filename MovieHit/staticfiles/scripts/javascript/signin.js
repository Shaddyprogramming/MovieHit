/**
 * MovieHit Authentication JavaScript
 * Handles sign-in and sign-up tab switching functionality
 */
document.addEventListener('DOMContentLoaded', function () {
    const tabs = document.querySelectorAll('.auth-tab');
    const forms = document.querySelectorAll('.auth-forms > div');
    const toggleLink = document.getElementById('toggle-form');
    const altText = document.querySelector('.auth-alt span');

    // Function to switch between signin and signup tabs
    function switchTab(tabId) {
        // Update tab active states
        tabs.forEach(tab => tab.classList.remove('active'));
        forms.forEach(form => form.classList.remove('active'));

        // Activate the selected tab and form
        document.querySelector(`.auth-tab[data-tab="${tabId}"]`).classList.add('active');
        document.getElementById(`${tabId}-form`).classList.add('active');

        // Update the toggle link text based on active tab
        if (tabId === 'signin') {
            altText.textContent = "Don't have an account?";
            toggleLink.textContent = "Create one now";
        } else {
            altText.textContent = "Already have an account?";
            toggleLink.textContent = "Sign in";
        }

        // Focus on the first input field of the active form
        setTimeout(() => {
            const firstInput = document.getElementById(`${tabId}-form`).querySelector('input');
            if (firstInput) firstInput.focus();
        }, 100);
    }

    // Set up tab click handlers
    tabs.forEach(tab => {
        tab.addEventListener('click', function () {
            switchTab(this.getAttribute('data-tab'));
        });
    });

    // Set up toggle link click handler
    toggleLink.addEventListener('click', function (e) {
        e.preventDefault();
        const activeTab = document.querySelector('.auth-tab.active').getAttribute('data-tab');
        switchTab(activeTab === 'signin' ? 'signup' : 'signin');
    });

    // Add form validation
    const signinForm = document.getElementById('signin-form');
    const signupForm = document.getElementById('signup-form');

    if (signinForm) {
        signinForm.addEventListener('submit', function (e) {
            const username = this.querySelector('input[name="username"]');
            const password = this.querySelector('input[name="password"]');

            if (!username.value.trim() || !password.value.trim()) {
                e.preventDefault();
                const errorEl = document.getElementById('signin-error') ||
                    createErrorElement(this, 'signin-error');
                errorEl.textContent = 'Please enter both username and password';
            }
        });
    }

    if (signupForm) {
        signupForm.addEventListener('submit', function (e) {
            const username = this.querySelector('input[name="username"]');
            const firstName = this.querySelector('input[name="first_name"]');
            const lastName = this.querySelector('input[name="last_name"]');
            const password = this.querySelector('input[name="password"]');
            const confirmPassword = this.querySelector('input[name="confirm_password"]');
            let hasError = false;
            let errorMessage = '';

            // Basic validation
            if (!username.value.trim() || !firstName.value.trim() ||
                !lastName.value.trim() || !password.value.trim() ||
                !confirmPassword.value.trim()) {
                hasError = true;
                errorMessage = 'All fields are required';
            } else if (password.value !== confirmPassword.value) {
                hasError = true;
                errorMessage = 'Passwords do not match';
            } else if (password.value.length < 8) {
                hasError = true;
                errorMessage = 'Password must be at least 8 characters';
            }

            if (hasError) {
                e.preventDefault();
                const errorEl = document.getElementById('signup-error') ||
                    createErrorElement(this, 'signup-error');
                errorEl.textContent = errorMessage;
            }
        });
    }

    // Helper function to create error element
    function createErrorElement(parent, id) {
        const errorEl = document.createElement('div');
        errorEl.className = 'error-message';
        errorEl.id = id;
        parent.prepend(errorEl);
        return errorEl;
    }
});
