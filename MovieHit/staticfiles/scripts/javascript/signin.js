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
});
