document.addEventListener('DOMContentLoaded', function () {
    const isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0;

    if (isTouchDevice) {
        const cards = document.querySelectorAll('.card');
        let touchStartY = 0;
        let touchEndY = 0;
        const minSwipeDistance = 10;

        cards.forEach(card => {
            const content = card.querySelector('.content');
            if (content) {
                content.style.pointerEvents = 'none';
            }

            let isScrolling = false;
            let isActive = false;

            card.addEventListener('touchstart', function (e) {
                touchStartY = e.touches[0].clientY;
            }, { passive: true });

            card.addEventListener('touchmove', function (e) {
                touchEndY = e.touches[0].clientY;
                const yDiff = Math.abs(touchEndY - touchStartY);

                if (yDiff > minSwipeDistance) {
                    isScrolling = true;
                }
            }, { passive: true });

            card.addEventListener('touchend', function (e) {
                if (isScrolling) {
                    isScrolling = false;
                } else {
                    e.preventDefault();
                    cards.forEach(c => {
                        c.classList.remove('touched');
                        const cContent = c.querySelector('.content');
                        if (cContent) cContent.style.pointerEvents = 'none';
                    });

                    this.classList.add('touched');
                    const thisContent = this.querySelector('.content');
                    if (thisContent) thisContent.style.pointerEvents = 'auto';

                    setTimeout(() => {
                        this.classList.remove('touched');
                        if (thisContent) thisContent.style.pointerEvents = 'none';
                    }, 3000);
                }
            });

            card.addEventListener('click', function (e) {
                const thisContent = this.querySelector('.content');
                if (!this.classList.contains('touched')) {
                    e.preventDefault();

                    cards.forEach(c => {
                        c.classList.remove('touched');
                        const cContent = c.querySelector('.content');
                        if (cContent) cContent.style.pointerEvents = 'none';
                    });

                    this.classList.add('touched');
                    if (thisContent) thisContent.style.pointerEvents = 'auto';

                    setTimeout(() => {
                        this.classList.remove('touched');
                        if (thisContent) thisContent.style.pointerEvents = 'none';
                    }, 3000);
                }
            });
        });

        document.addEventListener('click', function (e) {
            if (!e.target.closest('.card')) {
                cards.forEach(card => {
                    card.classList.remove('touched');
                    const content = card.querySelector('.content');
                    if (content) content.style.pointerEvents = 'none';
                });
            }
        });
    }
});
