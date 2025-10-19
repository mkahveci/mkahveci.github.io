/**
 * Copies the BibTeX citation associated with the clicked button to the clipboard.
 * @param {HTMLElement} buttonElement - The button element that was clicked.
 */
function copyBibtex(buttonElement) {
    // 1. Find the nearest hidden div containing the BibTeX data
    // It's the sibling to the button's parent div.
    const container = buttonElement.closest('.mt-2');
    const bibtexDataElement = container.querySelector('.bibtex-data');

    if (!bibtexDataElement) {
        console.error("BibTeX data element not found.");
        return;
    }

    // 2. Extract and clean the BibTeX text
    const bibtexText = bibtexDataElement.textContent.trim();

    // 3. Use the modern Clipboard API (async, cleaner)
    navigator.clipboard.writeText(bibtexText).then(() => {

        // 4. Provide temporary visual feedback
        const originalText = buttonElement.innerHTML;

        // Change button text/icon temporarily
        buttonElement.innerHTML = '<i class="fas fa-check fa-fw me-1"></i> Copied!';
        buttonElement.classList.add('btn-success');
        buttonElement.classList.remove('btn-outline-secondary');

        // Reset button after 2 seconds
        setTimeout(() => {
            buttonElement.innerHTML = originalText;
            buttonElement.classList.remove('btn-success');
            buttonElement.classList.add('btn-outline-secondary');
        }, 2000);

    }).catch(err => {
        console.error('Could not copy text: ', err);
        alert('Failed to copy BibTeX. Please select the text manually.');
    });
}