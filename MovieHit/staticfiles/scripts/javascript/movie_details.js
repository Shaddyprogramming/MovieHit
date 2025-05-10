/**
 * MovieHit - Movie Detail Page JavaScript
 * Enhanced version with improved UI handling and smoother transitions
 */

document.addEventListener('DOMContentLoaded', function () {
    // Initialize all components
    initTrailerPlayer();
    initCommentSystem();
    initDeleteConfirmation();
});

/**
 * Initialize and load trailer player if available
 */
function initTrailerPlayer() {
    const trailerContainer = document.getElementById('trailer-container');
    if (!trailerContainer) return;

    const trailerUrl = trailerContainer.dataset.trailerUrl;
    if (!trailerUrl || trailerUrl === "No trailer") return;

    const videoId = extractYouTubeVideoId(trailerUrl);
    if (!videoId) return;

    // Create and configure the iframe
    const iframe = document.createElement('iframe');
    iframe.src = `https://www.youtube.com/embed/${videoId}`;
    iframe.width = '100%';
    iframe.height = '100%';
    iframe.allowFullscreen = true;
    iframe.style.border = 'none'; // Modern approach instead of frameBorder

    trailerContainer.appendChild(iframe);
}

/**
 * Extract YouTube video ID from various URL formats
 */
function extractYouTubeVideoId(url) {
    if (!url) return null;

    // Handle various YouTube URL formats
    const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/;
    const match = url.match(regExp);

    return (match && match[2].length === 11) ? match[2] : null;
}

/**
 * Initialize the comment system including editing and rating functionalities
 */
function initCommentSystem() {
    // Initialize comment editing
    setupCommentEditing();

    // Set the selected ratings in dropdowns
    setupRatingSelections();
}

/**
 * Set up comment editing functionality with improved UI transitions
 */
function setupCommentEditing() {
    // Edit comment functionality
    const editButtons = document.querySelectorAll('.comment-edit-btn');

    editButtons.forEach(button => {
        button.addEventListener('click', function () {
            const commentId = this.dataset.commentId;
            const comment = document.getElementById(`comment-${commentId}`);
            if (!comment) return;

            // Store original height for smooth transitions
            const originalHeight = comment.offsetHeight;

            // Get elements
            const content = comment.querySelector('.comment-content');
            const editForm = comment.querySelector('.comment-edit-form');
            const actions = comment.querySelector('.comment-actions');

            // Ensure we have the needed elements
            if (!content || !editForm) return;

            // Set a minimum height to prevent collapse
            comment.style.minHeight = `${originalHeight}px`;

            // Apply transitions
            comment.classList.add('editing');

            // Show edit form, hide content and actions
            content.style.display = 'none';
            editForm.style.display = 'block';
            if (actions) actions.style.visibility = 'hidden';

            // Focus on the textarea
            const textarea = editForm.querySelector('textarea');
            if (textarea) {
                setTimeout(() => {
                    textarea.focus();
                    textarea.setSelectionRange(textarea.value.length, textarea.value.length);
                }, 0);
            }
        });
    });

    // Cancel edit functionality
    const cancelButtons = document.querySelectorAll('.comment-edit-cancel');

    cancelButtons.forEach(button => {
        button.addEventListener('click', function () {
            const commentId = this.dataset.commentId;
            const comment = document.getElementById(`comment-${commentId}`);
            if (!comment) return;

            // Get elements
            const content = comment.querySelector('.comment-content');
            const editForm = comment.querySelector('.comment-edit-form');
            const actions = comment.querySelector('.comment-actions');

            // Ensure we have the needed elements
            if (!content || !editForm) return;

            // Switch back to view mode
            content.style.display = 'block';
            editForm.style.display = 'none';
            if (actions) actions.style.visibility = 'visible';

            // Remove editing class
            comment.classList.remove('editing');

            // Reset height with transition after a delay
            setTimeout(() => {
                comment.style.transition = 'min-height 0.3s ease';
                comment.style.minHeight = '';

                // Remove transition after it completes
                setTimeout(() => {
                    comment.style.transition = '';
                }, 300);
            }, 10);
        });
    });
}

/**
 * Set the correct rating values in all rating dropdowns
 */
function setupRatingSelections() {
    const ratingSelects = document.querySelectorAll('select[data-current-rating]');

    ratingSelects.forEach(select => {
        const currentRating = select.dataset.currentRating;

        // Find and select the matching option
        for (let i = 0; i < select.options.length; i++) {
            if (select.options[i].value === currentRating) {
                select.options[i].selected = true;
                break;
            }
        }
    });
}

/**
 * Initialize delete confirmation modal and functionality
 */
function initDeleteConfirmation() {
    const deleteButtons = document.querySelectorAll('.comment-delete-btn');
    const modal = document.getElementById('delete-confirmation-modal');

    if (!modal) return;

    const confirmBtn = document.getElementById('confirm-delete-btn');
    const cancelBtn = document.getElementById('cancel-delete-btn');
    let activeDeleteForm = null;

    // Set up delete button click handlers
    deleteButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();

            // Get the delete form
            activeDeleteForm = this.closest('form');
            if (!activeDeleteForm) return;

            // Show the confirmation modal with fade-in effect
            modal.style.display = 'flex';
            modal.style.opacity = '0';

            // Trigger reflow to enable transition
            void modal.offsetWidth;

            modal.style.opacity = '1';
        });
    });

    // Confirm delete action
    if (confirmBtn) {
        confirmBtn.addEventListener('click', function () {
            if (activeDeleteForm) {
                activeDeleteForm.submit();
            }
            hideModal();
        });
    }

    // Cancel delete action
    if (cancelBtn) {
        cancelBtn.addEventListener('click', hideModal);
    }

    // Close modal when clicking outside
    modal.addEventListener('click', function (event) {
        if (event.target === modal) {
            hideModal();
        }
    });

    // Helper function to hide modal with fade-out effect
    function hideModal() {
        modal.style.opacity = '0';
        setTimeout(() => {
            modal.style.display = 'none';
            activeDeleteForm = null;
        }, 300);
    }

    // Close modal with ESC key
    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape' && modal.style.display === 'flex') {
            hideModal();
        }
    });
}

/**
 * Utility function to create a debounced function
 * that won't run until after a specified delay
 */
function debounce(func, delay) {
    let timeout;
    return function (...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), delay);
    };
}

/**
 * Add smooth scrolling to comment when URL contains comment hash
 */
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

// Initialize hash-based navigation if present
if (window.location.hash) {
    scrollToComment();
}

