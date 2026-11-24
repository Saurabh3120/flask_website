/**
 * FlaskCraft - Client-Side Interactions
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Mobile Navigation Drawer Toggle
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');

    if (navToggle && navMenu) {
        navToggle.addEventListener('click', () => {
            const isOpen = navMenu.classList.toggle('open');
            navToggle.classList.toggle('open');
            navToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
        });

        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!navToggle.contains(e.target) && !navMenu.contains(e.target) && navMenu.classList.contains('open')) {
                navMenu.classList.remove('open');
                navToggle.classList.remove('open');
                navToggle.setAttribute('aria-expanded', 'false');
            }
        });

        // Close menu on ESC key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && navMenu.classList.contains('open')) {
                navMenu.classList.remove('open');
                navToggle.classList.remove('open');
                navToggle.setAttribute('aria-expanded', 'false');
            }
        });
    }

    // 2. Auto-dismiss Flash Alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach((alert) => {
        setTimeout(() => {
            alert.style.transition = 'opacity 400ms ease, transform 400ms ease';
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-6px)';
            setTimeout(() => {
                if (alert.parentElement) {
                    alert.remove();
                }
            }, 400);
        }, 5000);
    });

    // 3. Form Submission UX Enhancement
    const contactForm = document.querySelector('.contact-form');
    const submitBtn = document.getElementById('submitBtn');

    if (contactForm && submitBtn) {
        contactForm.addEventListener('submit', (e) => {
            // Check form validity
            if (contactForm.checkValidity()) {
                submitBtn.disabled = true;
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<span>Sending message...</span>';
                
                // Allow form submit to continue
                setTimeout(() => {
                    // Safety fallback in case navigation is delayed
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalText;
                }, 8000);
            }
        });
    }

    // 4. Back to top smooth scroll
    const backToTopBtn = document.querySelector('.back-to-top');
    if (backToTopBtn) {
        backToTopBtn.addEventListener('click', (e) => {
            e.preventDefault();
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
});
