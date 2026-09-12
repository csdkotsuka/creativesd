/**
 * CSD Universal Header & Footer Embed Script
 * Enables affiliate.creativesd.net and manual.creativesd.net to dynamically load
 * the canonical header.html & footer.html from creativesd.net without duplicating code.
 */
(function() {
    const MAIN_SITE_URL = "https://creativesd.net/";

    // 1. Load Required CSS & Fonts
    function loadStyles() {
        // FontAwesome
        if (!document.querySelector('link[href*="font-awesome"]')) {
            const fa = document.createElement('link');
            fa.rel = 'stylesheet';
            fa.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css';
            document.head.appendChild(fa);
        }

        // Google Fonts Inter
        if (!document.querySelector('link[href*="fonts.googleapis.com/css2?family=Inter"]')) {
            const font = document.createElement('link');
            font.rel = 'stylesheet';
            font.href = 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap';
            document.head.appendChild(font);
        }

        // Main Site Style CSS
        const customStyle = document.createElement('link');
        customStyle.rel = 'stylesheet';
        customStyle.href = MAIN_SITE_URL + 'css/style.css?v=' + new Date().getTime();
        document.head.appendChild(customStyle);

        // Tailwind CSS CDN
        if (!window.tailwind) {
            const tw = document.createElement('script');
            tw.src = 'https://cdn.tailwindcss.com';
            tw.onload = () => {
                window.tailwind.config = {
                    theme: {
                        extend: {
                            colors: {
                                primary: '#004080',
                                secondary: '#00BCD4',
                                accent: '#FF6600',
                                glass: 'rgba(255, 255, 255, 0.7)',
                            },
                            fontFamily: {
                                sans: ['Inter', 'sans-serif'],
                            },
                        }
                    }
                };
            };
            document.head.appendChild(tw);
        }
    }

    // 2. Fetch & Render Header & Footer
    async function loadComponent(placeholderId, filename) {
        const placeholder = document.getElementById(placeholderId);
        if (!placeholder) return;

        try {
            const cacheBuster = '?v=' + new Date().getTime();
            const res = await fetch(MAIN_SITE_URL + filename + cacheBuster);
            if (res.ok) {
                let html = await res.text();
                // Replace [[ROOT]] placeholder with canonical main site URL
                html = html.replace(/\[\[ROOT\]\]/g, MAIN_SITE_URL);
                
                // Replace relative links in footer/header to point to main site (except affiliate link)
                html = html.replace(/href="index\.html"/g, `href="${MAIN_SITE_URL}index.html"`);
                html = html.replace(/href="atfirst\.html"/g, `href="${MAIN_SITE_URL}atfirst.html"`);
                html = html.replace(/href="update\.html"/g, `href="${MAIN_SITE_URL}update.html"`);
                html = html.replace(/href="system\.html"/g, `href="${MAIN_SITE_URL}system.html"`);
                html = html.replace(/href="plan\.html"/g, `href="${MAIN_SITE_URL}plan.html"`);
                html = html.replace(/href="contact\.html"/g, `href="${MAIN_SITE_URL}contact.html"`);
                html = html.replace(/href="privacy\.html"/g, `href="${MAIN_SITE_URL}privacy.html"`);
                html = html.replace(/href="terms\.html"/g, `href="${MAIN_SITE_URL}terms.html"`);
                html = html.replace(/href="sitemap\.html"/g, `href="${MAIN_SITE_URL}sitemap.html"`);
                html = html.replace(/src="assets\//g, `src="${MAIN_SITE_URL}assets/`);
                html = html.replace(/src="images\//g, `src="${MAIN_SITE_URL}images/`);

                placeholder.outerHTML = html;
            }
        } catch (e) {
            console.error("CSD Embed Component Load Error:", e);
        }
    }

    // 3. Initialize Interactive Features (Mobile Menu, Dropdowns, Search)
    function initInteractions() {
        // Mobile menu toggle
        const mobileToggle = document.getElementById('mobile-menu-toggle');
        const mobileMenu = document.getElementById('mobile-menu');
        if (mobileToggle && mobileMenu) {
            const icon = mobileToggle.querySelector('i');
            mobileToggle.addEventListener('click', () => {
                const isOpen = mobileMenu.style.maxHeight && mobileMenu.style.maxHeight !== '0px';
                if (isOpen) {
                    mobileMenu.style.maxHeight = '0px';
                    if (icon) { icon.classList.remove('fa-times'); icon.classList.add('fa-bars'); }
                } else {
                    mobileMenu.style.maxHeight = '600px';
                    if (icon) { icon.classList.remove('fa-bars'); icon.classList.add('fa-times'); }
                }
            });
        }

        // Systems Dropdown on click for mobile/touch
        const dropdownBtn = document.getElementById('systems-dropdown-btn');
        const dropdownMenu = document.getElementById('systems-dropdown-menu');
        if (dropdownBtn && dropdownMenu) {
            dropdownBtn.addEventListener('click', (e) => {
                if (window.innerWidth < 1024) {
                    e.preventDefault();
                    dropdownMenu.classList.toggle('hidden');
                }
            });
        }

        // Header shadow on scroll
        window.addEventListener('scroll', () => {
            const header = document.querySelector('header');
            if (header) {
                header.classList.toggle('shadow-lg', window.scrollY > 20);
            }
        });
    }

    // Run when DOM is ready
    async function init() {
        loadStyles();
        await Promise.all([
            loadComponent('csd-header-placeholder', 'header.html'),
            loadComponent('csd-footer-placeholder', 'footer.html')
        ]);
        initInteractions();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
