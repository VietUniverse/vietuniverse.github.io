document.addEventListener('DOMContentLoaded', function() {
    const menuButton = document.getElementById('menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    if(menuButton && mobileMenu) {
        menuButton.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });
    }

    const langToggleButton = document.getElementById('lang-toggle-btn');
    const essayEN = document.getElementById('essay-en');
    const essayVI = document.getElementById('essay-vi');

    if(langToggleButton && essayEN && essayVI) {
        langToggleButton.addEventListener('click', () => {
            const isVIVisible = !essayVI.classList.contains('hidden');
            if (isVIVisible) {
                essayVI.classList.add('hidden');
                essayEN.classList.remove('hidden');
                langToggleButton.textContent = 'Xem bản Tiếng Việt';
            } else {
                essayEN.classList.add('hidden');
                essayVI.classList.remove('hidden');
                langToggleButton.textContent = 'View English Version';
            }
        });
    }
    
    const currentYearSpan = document.getElementById('currentYear');
    if(currentYearSpan) {
        currentYearSpan.textContent = new Date().getFullYear();
    }

    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('header nav a.nav-link');
    const mobileNavLinks = document.querySelectorAll('#mobile-menu a');

    const makeLinkActive = (id) => {
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${id}`) {
                link.classList.add('active');
            }
        });
        mobileNavLinks.forEach(link => {
            if (link.getAttribute('href') === `#${id}`) {
            }
        });
    };

    mobileNavLinks.forEach(link => {
        link.addEventListener('click', () => {
            if(mobileMenu && !mobileMenu.classList.contains('hidden')) {
                mobileMenu.classList.add('hidden');
            }
        });
    });


    window.addEventListener('scroll', () => {
        let current = 'home';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            if (window.pageYOffset >= sectionTop - 70) {
                current = section.getAttribute('id');
            }
        });
        makeLinkActive(current);
    });

    const initialHash = window.location.hash.substring(1);
    if (initialHash) {
        makeLinkActive(initialHash);
    } else {
        makeLinkActive('home');
    }
});