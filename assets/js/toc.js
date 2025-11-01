document.addEventListener("DOMContentLoaded", function() {
    const tocContainer = document.getElementById("toc-container");
    const postContent = document.getElementById("post-content-container");
    const tocCard = document.getElementById("toc-placeholder");

    // Exit if the required elements aren't on the page
    if (!tocContainer || !postContent || !tocCard) {
        return;
    }

    // Find all h2 and h3 headings within the post content
    const headings = postContent.querySelectorAll("h2, h3");

    // If no headings are found, hide the entire TOC card and exit
    if (headings.length === 0) {
        tocCard.style.display = "none";
        return;
    }

    let tocList = document.createElement("ul");
    tocList.classList.add("toc"); // For styling

    let currentH2List = null; // To hold the <ul> for h3s under the current h2

    headings.forEach(function(heading) {
        // Ensure the heading has an ID. Kramdown usually provides one,
        // but this is a fallback.
        if (!heading.id) {
            heading.id = heading.textContent.toLowerCase()
                                .replace(/\s+/g, '-')
                                .replace(/[^\w-]+/g, '');
        }

        const id = heading.id;
        const text = heading.textContent;

        const listItem = document.createElement("li");
        const link = document.createElement("a");
        link.setAttribute("href", "#" + id);
        link.textContent = text;
        listItem.appendChild(link);

        if (heading.tagName === "H2") {
            // It's a top-level item
            tocList.appendChild(listItem);
            // Create a new nested list for any H3s that follow
            currentH2List = document.createElement("ul");
            listItem.appendChild(currentH2List);
        } else if (heading.tagName === "H3") {
            // It's a nested item
            if (currentH2List) {
                // Add to the current H2's nested list
                currentH2List.appendChild(listItem);
            } else {
                // It's an H3 with no H2 before it. Treat as top-level.
                tocList.appendChild(listItem);
            }
        }
    });

    // Clean up empty <ul> elements (if an H2 had no H3s)
    tocList.querySelectorAll("ul").forEach(ul => {
        if (ul.children.length === 0) {
            ul.remove();
        }
    });

    // Add the generated list to the container
    tocContainer.appendChild(tocList);
});