// main.js — students will add JavaScript here as features are built

// How It Works Modal
(function() {
    const modal = document.getElementById('how-it-works-modal');
    const openBtn = document.getElementById('how-it-works-btn');
    const closeBtn = document.getElementById('modal-close-btn');
    const videoFrame = document.getElementById('modal-video-frame');
    const VIDEO_URL = 'https://www.youtube.com/embed/dQw4w9WgXcQ?autoplay=1';

    if (!modal || !openBtn) return;

    function openModal() {
        modal.classList.add('active');
        videoFrame.src = VIDEO_URL;
        document.body.style.overflow = 'hidden';
    }

    function closeModal() {
        modal.classList.remove('active');
        videoFrame.src = '';
        document.body.style.overflow = '';
    }

    openBtn.addEventListener('click', openModal);
    closeBtn.addEventListener('click', closeModal);

    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeModal();
        }
    });

    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            closeModal();
        }
    });
})();
