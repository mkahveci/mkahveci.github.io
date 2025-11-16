---
layout: misc
title: Development Guide
date: 2025-11-16 13:24:00
mermaid: true
---

<div class="container my-5">
  <h1 class="bigtitle">Site Development Guide</h1>
  <p class="lead text-muted">A consolidated reference for common page components and automated workflows for kahveci.pw.</p>

  <hr class="my-5">

<h2 class="head fw-bold" id="components">Page Components & Includes</h2>
  <p>This section covers the standard Liquid includes for adding rich content to any page.</p>

<h3 class="h5 fw-bold text-body mt-4">Page Redirect</h3>
  <p>Add this to the front matter of a page to create a redirect from an old URL.</p>
  {% highlight yaml %}
  {% raw %}
  redirect_from:
  - /projectsgit/ai-in-education/
  {% endraw %}
  {% endhighlight %}

<h3 class="h5 fw-bold text-body mt-4">Related Protects Call Out</h3>
  <p>Adds a small "Related Project" box, typically at the top of a page or post.</p>
  {% highlight yaml %}
  {% raw %}
  related_project:
    name: "Quantitative Market Analysis (qma)"
    url: /projectsgit/qma/
  {% endraw %}
  {% endhighlight %}

<h3 class="h5 fw-bold text-body mt-4">Universal Figure Include (Image & Flowchart)</h3>
  <p>This single include can render either a <strong>standard image</strong> or a <strong>Mermaid flowchart</strong>, complete with automatic figure numbering (requires <code>figure_counter: 0</code> in the front matter).</p>

<h4>Standard Image</h4>
{% highlight liquid %}
{% raw %}
{% include figure.html
image_url='/images/blog/latex.jpg'
image_alt='Description of chart data.'
caption='This figure shows market volatility over three quarters.'
%}
{% endraw %}
{% endhighlight %}

<h4>Mermaid Flowchart (Left-to-Right)</h4>
{% highlight liquid %}
{% raw %}
{% include figure.html
mermaid_code='graph LR
A[Start] --> B(Process);
B --> C{Decision?};'
caption='A simple validation flowchart.'
%}
{% endraw %}
{% endhighlight %}

<h4>Mermaid Flowchart (Top-Down)</h4>
{% highlight liquid %}
{% raw %}
{% include figure.html
mermaid_code='graph TD
A[Start] --> B(Process);
B --> C{Decision?};'
caption='A simple validation flowchart.'
%}
{% endraw %}
{% endhighlight %}

<h3 class="h5 fw-bold text-body mt-4">Basic Callout Usage</h3>
  <p>Callouts are used to visually break up content and draw attention to important information. They use Bootstrap's <strong>d-flex</strong> layout (Icon on the left, content on the right).</p>

{% highlight liquid %}
{% raw %}
{% include callout.html
type="alert"
title='Publications Entry Alert'
content="Always verify collaborator search terms are in Last Name + Initial format (e.g., 'Kahveci M') for Publications/Projects filtering."
%}
{% endraw %}
{% endhighlight %}

<strong>Parameters</strong>
  <ul>
    <li><code>type</code>: <strong>(Required)</strong> Controls the color and icon. See available options below.</li>
    <li><code>title</code>: <strong>(Required)</strong> The <code>h5</code> heading inside the callout.</li>
    <li><code>content</code>: <strong>(Required)</strong> The body text.</li>
  </ul>

<strong>Available Types</strong>
  <div class="table-responsive">
    <table class="table">
      <thead>
        <tr>
          <th>Type</th>
          <th>Appearance</th>
          <th>Icon</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><code>note</code></td>
          <td>Primary, neutral information.</td>
          <td><i class="fas fa-sticky-note"></i></td>
        </tr>
        <tr>
          <td><code>info</code></td>
          <td>Detailed guidance or official data.</td>
          <td><i class="fas fa-info-circle"></i></td>
        </tr>
        <tr>
          <td><code>tip</code></td>
          <td>Best practice or helpful suggestion.</td>
          <td><i class="fas fa-lightbulb"></i></td>
        </tr>
        <tr>
          <td><code>warning</code></td>
          <td>Non-critical caution.</td>
          <td><i class="fas fa-exclamation-triangle"></i></td>
        </tr>
        <tr>
          <td><code>alert</code></td>
          <td>Critical requirement or error.</td>
          <td><i class="fas fa-exclamation-circle"></i></td>
        </tr>
      </tbody>
    </table>
  </div>

<h3 class="h5 fw-bold text-body mt-4">Buttons</h3>
{% highlight html %}
{% raw %}
<a href="/contact" class="btn btn-outline-primary"><i class="fas fa-envelope"></i> Contact</a>
<a href="/murat" class="btn btn-outline-secondary"><i class="fas fa-user-graduate"></i> Dr. Kahveci</a>
{% endraw %}
{% endhighlight %}

<h3 class="h5 fw-bold text-body mt-4">Adding an Image (Simple)</h3>
  <p>Note: This is an older include. For numbered figures, use the <strong>Universal Figure Include</strong> above.</p>
  {% highlight ruby %}
  {% raw %}
  {% include image.html
  file="/images/blog/latex.jpg"
  title="Figure 1."
  caption='Additional
  caption text.'
  width="250px"
  %}
  {% endraw %}
  {% endhighlight %}

<h3 class="h5 fw-bold text-body mt-4">List relevant posts by a tag</h3>
{% highlight ruby %}
{% raw %}
{% include list-relevant-posts.html tag="LaTeX Tweaks" %}
{% endraw %}
{% endhighlight %}

<h3 class="h5 fw-bold text-body mt-4">Icon links (the photo links)</h3>
  <p>These are placeholder URLs for generating the category-specific icons.</p>
  <ul>
    <li><strong>Journal Articles</strong>: <code>#0062B3</code></li>
  </ul>
  {% highlight liquid %}
  {% raw %}
  https://placehold.co/96x96/0062B3/ffffff?text=\n
  {% endraw %}
  {% endhighlight %}
  <ul>
    <li><strong>Books</strong>: <code>#800000</code></li>
  </ul>
  {% highlight liquid %}
  {% raw %}
  https://placehold.co/96x96/800000/ffffff?text=\n
  {% endraw %}
  {% endhighlight %}
  <ul>
    <li><strong>Conferences</strong>: <code>#6A0DAD</code></li>
  </ul>
  {% highlight liquid %}
  {% raw %}
  https://placehold.co/96x96/6A0DAD/ffffff?text=\n
  {% endraw %}
  {% endhighlight %}
  <ul>
    <li><strong>Talks</strong>: <code>#008080</code></li>
  </ul>
  {% highlight liquid %}
  {% raw %}
  https://placehold.co/96x96/008080/ffffff?text=\n
  {% endraw %}
  {% endhighlight %}
  <ul>
    <li><strong>Projects</strong>: <code>#006400</code></li>
  </ul>
  {% highlight liquid %} 
  {% raw %}
  https://placehold.co/96x96/006400/ffffff?text=\n
  {% endraw %}
  {% endhighlight %}
  <ul>
    <li><strong>Courses</strong>: <code>#FF4500</code></li>
  </ul>
  {% highlight liquid %}
  {% raw %}
  https://placehold.co/96x96/FF4500/ffffff?text=\n
  {% endraw %}
  {% endhighlight %}

<h3 class="h5 fw-bold text-body mt-4">Embed a PDF file</h3>
{% highlight ruby %}
{% raw %}
{% include pdf.html pdf_file="/pdfs/eu/FP7-SiS-2008-1-call.pdf" %}
{% endraw %}
{% endhighlight %}

  <hr class="my-5">

<h2 class="head fw-bold" id="workflow">GitHub Project Automation Workflow</h2>
  <p>This guide outlines the automated process for syncing content from your GitHub project repositories to your Jekyll site (<code>projectsgit/</code>), ensuring dynamic project listings, working links, and automated documentation.</p>

  ---

<h3>Part 1: Standardized Content Creation</h3>
  <p>Before running any script, all new project documentation and assets must be added to your GitHub repository.</p>

<h4>Step 1: Commit New Files to GitHub</h4>
  <ol>
    <li><strong>Create Project Repository:</strong> Ensure the repository exists on GitHub (e.g., <code>mkahveci/new-project</code>).</li>
    <li><strong>Add Documentation Folder:</strong> Inside your repository, create the standard content folder: <strong><code>docs/</code></strong> (all lowercase).</li>
    <li><strong>Add Content Files:</strong> Place all Markdown prompts (<code>.md</code>), guides, or documents inside this <code>docs/</code> folder.</li>
  </ol>

<h4>Step 2: Update the Project Listing</h4>
  <p>You must tell the build script which repositories to process by updating the configuration file.</p>
  <ol>
    <li><strong>Open</strong> the local <strong><code>_config.yml</code></strong> file in your Jekyll site root.</li>
    <li><strong>Add the new repository</strong> to the appropriate list (<code>projects</code> for full repos, <code>readmes</code> for documentation-only repos).</li>
  </ol>
  {% highlight yaml %}
  {% raw %}
  # Example _config.yml Update
  readmes:
    - mkahveci/ai-in-education
    - mkahveci/new-project-name # Add your new project here
  {% endraw %}
  {% endhighlight %}

<h4>Step 3: Update the Main README Table</h4>
  <p>For user readability, manually update the custom table in your GitHub repository's README.md file to include the link to the new prompt. Note: The links must point to the final .html file that Jekyll creates.</p>

{% highlight markdown %}
{% raw %}
| **Prompt Title** | **Focus Area** | **Description** | **Link** |
|-----------------------------------| ----- | ----- |---------------------------------------------------------------------------------|  
| **Socratic Chemistry Tutor** | Stoichiometry | Guides students through complex calculations step-by-step using only guiding questions. | [View Prompt](/projectsgit/ai-in-education/docs/socratic_chemistry_tutor)                  |
| **ELL Text Simplifier  & Vocabulary Scaffolder** | Vocabulary / Reading | Takes a dense scientific paragraph and outputs a simplified version with a target vocabulary list. | [View Prompt](/projectsgit/ai-in-education/docs/ell_text_simplifier)  |
| .. | .. | .. | .. |
{% endraw %}
{% endhighlight %}

  ---

<h3>Part 2: Automated Build and Synchronization</h3>
  <p>Execute this single command from your Jekyll site root directory (mkahveci.github.io/) after making any remote changes.</p>

<strong>Full Workflow Command</strong>
{% highlight bash %}
{% raw %}
ruby _scripts/build_projects.rb
{% endraw %}
{% endhighlight %}

<h4>Script Actions (Executed Sequentially)</h4>
  <ol>
  <li><strong>Download & Clean (ReadmeDownloader):</strong>
     <ul>
      <li>Connects to GitHub and downloads the main README.md and all files within the docs/ folder for every listed project.</li>
      <li>Creates the necessary local folder structure (e.g., projectsgit/ai-in-education/docs/).</li>
      <li>Handles GitHub caching issues and attempts to download the file directly if the API directory check fails.</li>
      <li>Automatically creates the docs/index.html redirect page to handle manual URL lookups.</li>
     </ul>
  </li>
  <li><strong>Preprocess Markdown (MarkdownPreprocessor):</strong>
      <ul>
      <li><strong>Adds Front Matter:</strong> Scans all .md files (including new ones in docs/) and inserts the required YAML Front Matter (<code>--- layout: projectgit ---</code>).</li>
      <li><strong>Renames Index:</strong> Renames README.md to index.md for clean URLs.</li>
      <li><strong>Fixes Links:</strong> Converts all internal .md links to .html links, and converts source code links to direct GitHub URLs.</li>
     </ul>
  </li>
  <li><strong>Generate Data (DataGenerator):</strong>
      <ul>
      <li>Connects to the GitHub API to fetch repository metadata (description, contributors, latest commit).</li>
      <li>Writes all aggregated data to _data/projectsgit.yml, which powers your main project listing page.</li>
     </ul>
  </li>
  <li><strong>Finalize:</strong> Once the script is complete, start your Jekyll server.</li>
  </ol>

{% highlight bash %}
{% raw %}
jekyll serve
{% endraw %}
{% endhighlight %}

  ---

<h3>Part 3: Custom Prompt Template</h3>
  <p>Use this template as the base for all new Markdown prompt files you place in your <code>docs/</code> folder.</p>

{% highlight markdown %}
{% raw %}
  ---
layout: projectgit
title: [Short_Descriptive_Title_Lowercase]
project: [REPLACE WITH REPO NAME, e.g., ai-in-education]
repo: [REPLACE WITH FULL REPO PATH, e.g., mkahveci/ai-in-education]
permalink: /:path/:basename:output_ext
  ---

## [Clear, User-Facing Title]

This prompt is designed for [Specify audience and academic level, e.g., undergraduate research or high school review].

### System Role/Persona:

[Define the AI's persona, expertise, and constraints. This is the core instruction.]
You are an unbiased, expert, and patient Socratic guide specializing in [Subject Area]. You must never give the direct answer.

### Primary Task Instruction:

[Provide the main task instruction for the user to copy/paste along with the text.]

Analyze the following text and explain the concept of [Concept] using two paragraphs of standard reading difficulty.

[PASTE ORIGINAL TEXT HERE]
{% endraw %}
{% endhighlight %}

</div>