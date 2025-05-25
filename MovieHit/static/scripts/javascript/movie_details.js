document.addEventListener('DOMContentLoaded', function () {
    initTrailerPlayer();
    initCommentSystem();
    initDeleteConfirmation();
});

function initTrailerPlayer() {
    const trailerContainer = document.getElementById('trailer-container');
    if (!trailerContainer) return;

    const trailerUrl = trailerContainer.dataset.trailerUrl;
    if (!trailerUrl || trailerUrl === "No trailer") return;

    const videoId = extractYouTubeVideoId(trailerUrl);
    if (!videoId) return;

    const autoplay = localStorage.getItem('autoplayTrailers') === 'true';

    const iframe = document.createElement('iframe');

    if (autoplay) {
        iframe.src = `https://www.youtube.com/embed/${videoId}?autoplay=1&mute=1`;
        iframe.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
    } else {
        iframe.src = `https://www.youtube.com/embed/${videoId}`;
    }

    iframe.width = '100%';
    iframe.height = '100%';
    iframe.allowFullscreen = true;
    iframe.style.border = 'none';

    trailerContainer.appendChild(iframe);

    if (autoplay) {
        const autoplayIndicator = document.createElement('div');
        autoplayIndicator.className = 'autoplay-indicator';
        autoplayIndicator.textContent = 'Autoplay On';
        autoplayIndicator.style.position = 'absolute';
        autoplayIndicator.style.top = '10px';
        autoplayIndicator.style.right = '10px';
        autoplayIndicator.style.background = 'rgba(0, 0, 0, 0.6)';
        autoplayIndicator.style.color = 'white';
        autoplayIndicator.style.padding = '5px 10px';
        autoplayIndicator.style.borderRadius = '4px';
        autoplayIndicator.style.fontSize = '12px';
        autoplayIndicator.style.opacity = '1';
        autoplayIndicator.style.transition = 'opacity 0.5s';

        trailerContainer.style.position = 'relative';
        trailerContainer.appendChild(autoplayIndicator);

        setTimeout(() => {
            autoplayIndicator.style.opacity = '0';
        }, 3000);
    }
}

function extractYouTubeVideoId(url) {
    if (!url) return null;

    const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/;
    const match = url.match(regExp);

    return (match && match[2].length === 11) ? match[2] : null;
}

function initCommentSystem() {
    setupCommentEditing();

    setupRatingSelections();
}

function setupCommentEditing() {
    const editButtons = document.querySelectorAll('.comment-edit-btn');

    editButtons.forEach(button => {
        button.addEventListener('click', function () {
            const commentId = this.dataset.commentId;
            const comment = document.getElementById(`comment-${commentId}`);
            if (!comment) return;

            const originalHeight = comment.offsetHeight;

            const content = comment.querySelector('.comment-content');
            const editForm = comment.querySelector('.comment-edit-form');
            const actions = comment.querySelector('.comment-actions');

            if (!content || !editForm) return;

            comment.style.minHeight = `${originalHeight}px`;

            comment.classList.add('editing');

            content.style.display = 'none';
            editForm.style.display = 'block';
            if (actions) actions.style.visibility = 'hidden';

            const textarea = editForm.querySelector('textarea');
            if (textarea) {
                setTimeout(() => {
                    textarea.focus();
                    textarea.setSelectionRange(textarea.value.length, textarea.value.length);
                }, 0);
            }
        });
    });

    const cancelButtons = document.querySelectorAll('.comment-edit-cancel');

    cancelButtons.forEach(button => {
        button.addEventListener('click', function () {
            const commentId = this.dataset.commentId;
            const comment = document.getElementById(`comment-${commentId}`);
            if (!comment) return;

            const content = comment.querySelector('.comment-content');
            const editForm = comment.querySelector('.comment-edit-form');
            const actions = comment.querySelector('.comment-actions');

            if (!content || !editForm) return;

            content.style.display = 'block';
            editForm.style.display = 'none';
            if (actions) actions.style.visibility = 'visible';

            comment.classList.remove('editing');

            setTimeout(() => {
                comment.style.transition = 'min-height 0.3s ease';
                comment.style.minHeight = '';

                setTimeout(() => {
                    comment.style.transition = '';
                }, 300);
            }, 10);
        });
    });
}

function setupRatingSelections() {
    const ratingSelects = document.querySelectorAll('select[data-current-rating]');

    ratingSelects.forEach(select => {
        const currentRating = select.dataset.currentRating;

        for (let i = 0; i < select.options.length; i++) {
            if (select.options[i].value === currentRating) {
                select.options[i].selected = true;
                break;
            }
        }
    });
}

function initDeleteConfirmation() {
    const deleteButtons = document.querySelectorAll('.comment-delete-btn');
    const modal = document.getElementById('delete-confirmation-modal');

    if (!modal) return;

    const confirmBtn = document.getElementById('confirm-delete-btn');
    const cancelBtn = document.getElementById('cancel-delete-btn');
    let activeDeleteForm = null;

    deleteButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();

            activeDeleteForm = this.closest('form');
            if (!activeDeleteForm) return;

            modal.style.display = 'flex';
            modal.style.opacity = '0';

            void modal.offsetWidth;

            modal.style.opacity = '1';
        });
    });

    if (confirmBtn) {
        confirmBtn.addEventListener('click', function () {
            if (activeDeleteForm) {
                activeDeleteForm.submit();
            }
            hideModal();
        });
    }

    if (cancelBtn) {
        cancelBtn.addEventListener('click', hideModal);
    }

    modal.addEventListener('click', function (event) {
        if (event.target === modal) {
            hideModal();
        }
    });

    function hideModal() {
        modal.style.opacity = '0';
        setTimeout(() => {
            modal.style.display = 'none';
            activeDeleteForm = null;
        }, 300);
    }

    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape' && modal.style.display === 'flex') {
            hideModal();
        }
    });
}


function debounce(func, delay) {
    let timeout;
    return function (...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), delay);
    };
}

function scrollToComment() {
    if (window.location.hash && window.location.hash.includes('comment-')) {
        const commentId = window.location.hash.substring(1);
        const comment = document.getElementById(commentId);

        if (comment) {
            setTimeout(() => {
                comment.scrollIntoView({ behavior: 'smooth', block: 'center' });
                comment.classList.add('highlight');

                setTimeout(() => {
                    comment.classList.remove('highlight');
                }, 3000);
            }, 500);
        }
    }
}

if (window.location.hash) {
    scrollToComment();
}
