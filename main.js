// REGISTER GSAP PLUGINS
gsap.registerPlugin(ScrollTrigger);

// HEADER SCROLL BEHAVIOR
let lastScroll = 0;
const header = document.querySelector('.site-header');

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;

    if (currentScroll > lastScroll && currentScroll > 100) {
        // Scroll Down
        header.classList.add('hidden');
    } else {
        // Scroll Up
        header.classList.remove('hidden');
    }
    lastScroll = currentScroll;
});

// REVEAL ANIMATIONS
const revealElements = document.querySelectorAll('.reveal-text, .reveal-card, .reveal-image');

// STANDARD TEXT REVEAL
gsap.utils.toArray('.reveal-text').forEach(element => {
    gsap.fromTo(element,
        {
            y: 30,
            opacity: 0
        },
        {
            y: 0,
            opacity: 1,
            duration: 0.8,
            ease: "power2.out",
            scrollTrigger: {
                trigger: element,
                start: "top 90%", // Start when top of element hits 90% of viewport
                toggleActions: "play none none reverse"
            }
        }
    );
});

// CARD STAGGERED REVEAL
// Find all container sections that have cards
const cardSections = document.querySelectorAll('.grid');

cardSections.forEach(section => {
    const cards = section.querySelectorAll('.reveal-card, .card');
    if (cards.length > 0) {
        gsap.fromTo(cards,
            {
                y: 40,
                opacity: 0
            },
            {
                y: 0,
                opacity: 1,
                duration: 0.8,
                stagger: 0.1, // Stagger delays
                ease: "power2.out",
                scrollTrigger: {
                    trigger: section,
                    start: "top 85%",
                    toggleActions: "play none none reverse"
                }
            }
        );
    }
});

// IMAGE REVEAL (Clip Path)
gsap.utils.toArray('.reveal-image').forEach(element => {
    gsap.fromTo(element,
        {
            opacity: 0,
            clipPath: "inset(0 100% 0 0)" // Hidden (clipped fully)
        },
        {
            opacity: 1,
            clipPath: "inset(0 0% 0 0)", // Fully visible
            duration: 1.2,
            ease: "power2.inOut",
            scrollTrigger: {
                trigger: element,
                start: "top 80%",
                toggleActions: "play none none reverse"
            }
        }
    );
});

// TEXT BLUR ANIMATION (MagicUI Style)
function splitAndAnimateHero(element) {
    // Prevent re-running if already split
    if (element.getAttribute('data-split')) return;
    element.setAttribute('data-split', 'true');

    const originalHTML = element.innerHTML;
    // Basic split by <br> tags to preserve structure
    // We handle text nodes by splitting into words

    // We'll rebuild the content
    element.innerHTML = '';
    const childSpans = [];

    // Helper to process text string
    const processText = (text) => {
        const words = text.split(/\s+/); // Split by whitespace
        words.forEach((word, index) => {
            if (!word) return;
            const span = document.createElement('span');
            span.textContent = word;
            // Add a trailing space unless it's the last word of this chunk
            // Actually simply adding margin-right or a separate space node is safer for layout
            // But for simplicity, we'll append a space node after

            span.style.display = 'inline-block';
            span.style.opacity = '0';
            span.style.filter = 'blur(10px)';
            span.style.transform = 'translateY(10px) scale(1.1)'; // Slight scale and Y offset
            span.style.willChange = 'transform, opacity, filter';
            span.style.marginRight = '0.25em'; // Space between words

            element.appendChild(span);
            childSpans.push(span);
        });
    };

    // Simple parser for <br>
    const parts = originalHTML.split(/<br\s*\/?>/i);
    parts.forEach((part, index) => {
        // Strip HTML tags from part if strictly text desired, 
        // but here we assume part is text. If H1 has mixed tags, this is fragile.
        // Assuming simple text + <br>.
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = part;
        processText(tempDiv.textContent); // Get clean text

        // Add BR if not last part
        if (index < parts.length - 1) {
            const br = document.createElement('br');
            element.appendChild(br);
        }
    });

    // Animate
    gsap.to(childSpans, {
        opacity: 1,
        filter: 'blur(0px)',
        scale: 1,
        y: 0,
        duration: 0.8,
        stagger: 0.05,
        ease: "power2.out",
        delay: 0.2, // Wait slightly for panel
        scrollTrigger: {
            trigger: element,
            start: "top 90%"
        }
    });
}

// Target all H1s and specific hero texts
document.addEventListener('DOMContentLoaded', () => {
    const mainTexts = document.querySelectorAll('h1, .hero-text-blur');
    mainTexts.forEach(splitAndAnimateHero);

    // MOBILE MENU LOGIC
    const hamburgerBtn = document.querySelector('.hamburger-btn');
    const closeBtn = document.querySelector('.close-btn');
    const overlay = document.querySelector('.mobile-nav-overlay');
    const dropdowns = document.querySelectorAll('.mobile-dropdown');

    if (hamburgerBtn && overlay) {
        hamburgerBtn.addEventListener('click', () => {
            overlay.classList.add('is-open');
            document.body.style.overflow = 'hidden'; // Prevent scroll
        });
    }

    if (closeBtn && overlay) {
        closeBtn.addEventListener('click', () => {
            overlay.classList.remove('is-open');
            document.body.style.overflow = ''; // Restore scroll
        });
    }

    // Accordion logic (Level 2)
    dropdowns.forEach(dropdown => {
        const link = dropdown.querySelector('.overlay-link');
        link.addEventListener('click', (e) => {
            e.preventDefault();
            dropdown.classList.toggle('is-expanded');
        });
    });

    // Level 3 Mobile Accordion logic
    const innerDropdowns = document.querySelectorAll(".mobile-dropdown-inner");
    innerDropdowns.forEach(inner => {
        const btn = inner.querySelector(".submenu-parent-link");
        if (btn) {
            btn.addEventListener("click", (e) => {
                e.preventDefault();
                inner.classList.toggle("is-open");
            });
        }
    });
});
