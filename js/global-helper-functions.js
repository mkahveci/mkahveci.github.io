'use strict';

// ==========================================================
// 1. GLOBAL HELPER FUNCTIONS
// ==========================================================

/**
 * --- NEW FUNCTION ---
 * Generates BibTeX on-the-fly from data attributes
 * and copies it to the clipboard.
 */
function generateAndCopyBibtex(button) {
    const originalHTML = button.innerHTML;
    const data = button.dataset;

    try {
        // 1. Get data from attributes
        const type = data.type || 'misc'; // 'article', 'inproceedings'
        const id = data.id || `temp${new Date().getTime()}`;
        const title = data.title || 'No Title';
        const year = data.year || 'YYYY';

        // 2. Format authors: "A, B, C" -> "A and B and C"
        const authors = (data.authors || 'No Authors').replace(/, /g, ' and ');

        // 3. Handle source info based on type
        let sourceField = '';
        const source = data.source || 'Unknown';

        if (type === 'article') {
            sourceField = `  journal   = {${source}},\n`;
        } else if (type === 'inproceedings') {
            sourceField = `  booktitle = {${source}},\n`;
        } else {
            sourceField = `  howpublished = {${source}},\n`;
        }

        // 4. Build the BibTeX string
        const bibtexString = `@${type}{${id},
title     = {${title}},
author    = {${authors}},
year      = {${year}},
${sourceField}
}`;

        // 5. Copy to clipboard
        navigator.clipboard.writeText(bibtexString.trim()).then(() => {
            // Show Success
            button.innerHTML = '<i class="fas fa-check fa-fw me-1"></i> Copied!';
            button.classList.add('btn-success');
            button.classList.remove('btn-outline-primary', 'btn-outline-secondary');

            // Restore after 2 seconds
            setTimeout(() => {
                button.innerHTML = originalHTML;
                button.classList.remove('btn-success');
                button.classList.add('btn-outline-primary');
            }, 2000);
        }).catch(err => {
            throw new Error('Clipboard write failed: ' + err);
        });

    } catch (err) {
        console.error('Failed to copy BibTeX: ', err);
        // Show a generic error
        button.innerHTML = '<i class="fas fa-times fa-fw me-1"></i> Error';
        button.classList.add('btn-danger');
        button.classList.remove('btn-outline-primary', 'btn-outline-secondary');

        // Restore after 2 seconds
        setTimeout(() => {
            button.innerHTML = originalHTML;
            button.classList.remove('btn-danger');
            button.classList.add('btn-outline-primary');
        }, 2000);
    }
}


/**
 * Theme Toggler function
 */
function initThemeToggler(button) {
    const THEME_STORAGE_KEY = 'kahveci-pw-theme';
    const sunIcon = button.querySelector('.fa-sun');
    const moonIcon = button.querySelector('.fa-moon');
    const currentTheme = document.documentElement.getAttribute('data-bs-theme');

    sunIcon.classList.toggle('d-none', currentTheme === 'light');
    moonIcon.classList.toggle('d-none', currentTheme === 'dark');

    button.addEventListener('click', () => {
        const newTheme = document.documentElement.getAttribute('data-bs-theme') === 'dark' ? 'light' : 'dark';
        localStorage.setItem(THEME_STORAGE_KEY, newTheme);
        document.documentElement.setAttribute('data-bs-theme', newTheme);
        sunIcon.classList.toggle('d-none', newTheme === 'light');
        moonIcon.classList.toggle('d-none', newTheme === 'dark');
    });
}

// ==========================================================
// 2. DOM-DEPENDENT CODE
// (This runs only *after* the HTML page is fully loaded)
// ==========================================================
document.addEventListener('DOMContentLoaded', () => {

  // --- Dynamic Year Script ---
  const currentYearEl = document.getElementById('current-year');
  if (currentYearEl) {
      currentYearEl.textContent = new Date().getFullYear();
  }

  // --- Modern Scroll to Top Script ---
  const scrollToTopBtn = document.getElementById('scrollToTopBtn');
  if (scrollToTopBtn) {
    // Show or hide the button based on scroll position
    window.addEventListener('scroll', () => {
      const isScrolled = document.body.scrollTop > 200 || document.documentElement.scrollTop > 200;
      scrollToTopBtn.classList.toggle('show', isScrolled);
    });

    // Smoothly scroll to the top when the button is clicked
    scrollToTopBtn.addEventListener('click', () => {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  }

  // --- Theme Toggler Initialization ---
  const themeToggler = document.getElementById('theme-toggler');
  if (themeToggler) {
      initThemeToggler(themeToggler);
  }
});