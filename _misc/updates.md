---
layout: misc
title: All Commits by Repos
date: 2025-11-02 00:00:00
permalink: /updates/
---

<div class="container my-5">

    <p class="lead text-center text-muted mb-5">
        A filterable list of all recent commits, grouped by repository.
    </p>

    <div class="mb-4 d-flex justify-content-end">
        <div class="repo-filter-container">
            <label for="repo-selector" class="form-label d-none d-lg-inline-block small text-muted me-2 mb-0">Filter by Repository:</label>
            <select id="repo-selector" class="form-select form-select-sm d-inline-block w-auto"></select>
        </div>
    </div>

    <div id="commit-list" class="row row-cols-1 row-cols-md-2 g-3">
        </div>

</div>

<script>
    document.addEventListener("DOMContentLoaded", () => {
      // --- 1. SETUP ---
      const commits = {{ site.data.repo_commits | jsonify }};
      const selector = document.getElementById("repo-selector");
      const list = document.getElementById("commit-list");

      // Use Intl.Collator for perfect case-insensitive sorting (like your blog)
      const collator = new Intl.Collator(undefined, { sensitivity: 'base' });
      
      // Get a unique, sorted list of all repository names
      const repos = [...new Set(commits.map(c => c.repo))];
      repos.sort(collator.compare);

      // --- 2. DATE FORMATTING FUNCTION ---
      function formatCommitDate(dateString) {
        const date = new Date(dateString);
        const options = { 
          month: 'short', 
          day: '2-digit', 
          year: 'numeric', 
          hour: '2-digit', 
          minute: '2-digit', 
          hour12: false 
        };
        const parts = new Intl.DateTimeFormat('en-US', options).formatToParts(date);
        const map = Object.fromEntries(parts.map(p => [p.type, p.value]));
        return `${map.month} ${map.day}, ${map.year} ${map.hour}:${map.minute}`;
      }

      // --- 3. POPULATE DROPDOWN ---
      function populateDropdown() {
        // "All Repos" option
        const allOpt = document.createElement("option");
        allOpt.value = "all";
        allOpt.textContent = `All Repos (${commits.length})`;
        selector.appendChild(allOpt);

        // One option for each repo
        repos.forEach(repo => {
          const repoCommitCount = commits.filter(c => c.repo === repo).length;
          const opt = document.createElement("option");
          opt.value = repo;
          opt.textContent = `${repo} (${repoCommitCount})`;
          selector.appendChild(opt);
        });
      }

      // --- 4. RENDER COMMITS (Unchanged from before) ---
      function renderCommits(repoName = null) {
        list.innerHTML = ""; // Clear the list
        let filtered = repoName ? commits.filter(c => c.repo === repoName) : commits;
        
        filtered.slice(0, 200).forEach(c => {
          const col = document.createElement("div");
          col.className = "col";
          const formattedDate = formatCommitDate(c.date);

          col.innerHTML = `
            <div class="card shadow-sm h-100 border-0 d-flex flex-column">
                <div class="card-body d-flex flex-grow-1">
                    <div class="flex-shrink-0 text-center text-muted" style="width: 50px;">
                        <i class="fas fa-code-commit fa-2x"></i>
                    </div>
                    <div class="flex-grow-1 ms-3">
                        <h6 class="mb-1">
                            <a href="${c.url}" target="_blank" rel="noopener noreferrer" class="text-decoration-none text-body">${c.message}</a>
                        </h6>
                        <small class="text-primary fw-bold font-monospace">${c.repo}</small>
                        <div class="small text-muted mt-2">
                            <i class="fas fa-user fa-fw" title="Author"></i> ${c.author}
                            <i class="fas fa-calendar-alt fa-fw ms-3" title="Date"></i> ${formattedDate}
                        </div>
                    </div>
                </div>
            </div>
          `;
          list.appendChild(col);
        });
      }

      // --- 5. EVENT LISTENER ---
      selector.addEventListener("change", () => {
        const selectedRepo = selector.value === "all" ? null : selector.value;
        renderCommits(selectedRepo);
      });

      // --- 6. INITIAL LOAD ---
      populateDropdown(); // Build the dropdown
      renderCommits();    // Show "All Repos" by default
    });
</script>