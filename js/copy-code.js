document.addEventListener("DOMContentLoaded", function () {
    // Find all <pre><code> blocks generated by Markdown
    const codeBlocks = document.querySelectorAll("pre code");

    codeBlocks.forEach((codeElement) => {
        // Get the parent <pre> element
        const preElement = codeElement.parentNode;

        // Get the language from the <code> class (e.g., "language-javascript")
        const classList = codeElement.className.split(" ");
        const languageClass = classList.find((cls) => cls.startsWith("language-"));
        const language = languageClass ? languageClass.replace("language-", "") : "Code";

        // Create a wrapper for the <pre> block
        const wrapper = document.createElement("div");
        wrapper.className = "code-snippet";
        wrapper.setAttribute("data-code-type", language);

        // Create a header with the code type and copy button
        const header = document.createElement("div");
        header.className = "code-header";
        header.innerHTML = `
            <span class="code-type">${language}</span>
            <button class="copy-button">&#9635; Copy Code</button>
        `;

        // Add the header and move the <pre> block into the wrapper
        wrapper.appendChild(header);
        wrapper.appendChild(preElement.cloneNode(true));
        preElement.replaceWith(wrapper);

        // Add functionality to the copy button
        const copyButton = wrapper.querySelector(".copy-button");
        copyButton.addEventListener("click", () => {
            // Get the text content of the code block
            const codeText = codeElement.innerText;

            // Create a temporary textarea to copy the code
            const tempTextarea = document.createElement("textarea");
            tempTextarea.value = codeText;
            document.body.appendChild(tempTextarea);

            // Select and copy the text
            tempTextarea.select();
            document.execCommand("copy");

            // Remove the temporary textarea
            document.body.removeChild(tempTextarea);

            // Provide user feedback
            copyButton.textContent = "Copied!";
            setTimeout(() => (copyButton.innerHTML = "&#9635; Copy Code"), 2000);
        });
    });
});