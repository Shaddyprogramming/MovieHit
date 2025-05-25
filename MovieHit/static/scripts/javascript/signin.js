document.addEventListener('DOMContentLoaded', function () {
    const tabs = document.querySelectorAll('.auth-tab');
    const forms = document.querySelectorAll('.auth-forms > div');
    const toggleLink = document.getElementById('toggle-form');
    const altText = document.querySelector('.auth-alt span');

    function switchTab(tabId) {
        tabs.forEach(tab => tab.classList.remove('active'));
        forms.forEach(form => form.classList.remove('active'));

        document.querySelector(`.auth-tab[data-tab="${tabId}"]`).classList.add('active');
        document.getElementById(`${tabId}-form`).classList.add('active');

        if (tabId === 'signin') {
            altText.textContent = "Don't have an account?";
            toggleLink.textContent = "Create one now";
        } else {
            altText.textContent = "Already have an account?";
            toggleLink.textContent = "Sign in";
        }

        setTimeout(() => {
            const firstInput = document.getElementById(`${tabId}-form`).querySelector('input');
            if (firstInput) firstInput.focus();
        }, 100);
    }

    tabs.forEach(tab => {
        tab.addEventListener('click', function () {
            switchTab(this.getAttribute('data-tab'));
        });
    });

    toggleLink.addEventListener('click', function (e) {
        e.preventDefault();
        const activeTab = document.querySelector('.auth-tab.active').getAttribute('data-tab');
        switchTab(activeTab === 'signin' ? 'signup' : 'signin');
    });

    const signinForm = document.getElementById('signin-form');
    const signupForm = document.getElementById('signup-form');

    const passwordInput = document.getElementById('new-password');
    const confirmInput = document.getElementById('confirm-password');
    const passwordMessage = document.getElementById('password-match-message');

    if (passwordInput && confirmInput && passwordMessage) {
        function validatePasswords() {
            if (confirmInput.value && passwordInput.value !== confirmInput.value) {
                confirmInput.classList.add('invalid');
                passwordMessage.classList.add('visible');
                return false;
            } else {
                confirmInput.classList.remove('invalid');
                passwordMessage.classList.remove('visible');
                return true;
            }
        }

        confirmInput.addEventListener('input', validatePasswords);
        passwordInput.addEventListener('input', validatePasswords);
        confirmInput.addEventListener('blur', validatePasswords);
    }

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
            const email = this.querySelector('input[name="email"]');
            let hasError = false;
            let errorMessage = '';

            if (!username.value.trim() || !firstName.value.trim() ||
                !lastName.value.trim() || !password.value.trim() ||
                !confirmPassword.value.trim() || !email.value.trim()) {
                hasError = true;
                errorMessage = 'All fields are required';
            } else if (password.value !== confirmPassword.value) {
                hasError = true;
                errorMessage = 'Passwords do not match';
                confirmPassword.classList.add('invalid');
                passwordMessage.classList.add('visible');
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

    function createErrorElement(parent, id) {
        const errorEl = document.createElement('div');
        errorEl.className = 'error-message';
        errorEl.id = id;
        parent.prepend(errorEl);
        return errorEl;
    }
});
