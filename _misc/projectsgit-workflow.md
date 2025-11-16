---
layout: misc
title: Code Snippets
date: 2025-09-28 00:00:00
permalink: /pgit-workflow
---

# Jekyll Automation Workflow for GitHub Projects

This guide outlines the automated process for syncing content from your GitHub project repositories to your Jekyll site (`projectsgit/`), ensuring dynamic project listings, working links, and automated documentation.

---

## Part 1: Standardized Content Creation

Before running any script, all new project documentation and assets must be added to your GitHub repository.

### Step 1: Commit New Files to GitHub

1.  **Create Project Repository:** Ensure the repository exists on GitHub (e.g., `mkahveci/new-project`).
2.  **Add Documentation Folder:** Inside your repository, create the standard content folder: **`docs/`** (all lowercase).
3.  **Add Content Files:** Place all Markdown prompts (`.md`), guides, or documents inside this `docs/` folder.

### Step 2: Update the Project Listing

You must tell the build script which repositories to process by updating the configuration file.

1.  **Open** the local **`_config.yml`** file in your Jekyll site root.
2.  **Add the new repository** to the appropriate list (`projects` for full repos, `readmes` for documentation-only repos).

```yaml
# Example _config.yml Update
readmes:
  - mkahveci/ai-in-education
  - mkahveci/new-project-name # Add your new project here
```

### Step 3: Update the Main README Table

For user readability, manually update the custom table in your GitHub repository's README.md file to include the link to the new prompt. Note: The links must point to the final .html file that Jekyll creates.

| **Prompt Title**                  | **Focus Area** | **Description** | **Link**                                                                        | 
 |-----------------------------------| ----- | ----- |---------------------------------------------------------------------------------|  
| **Socratic Chemistry Tutor**      | Stoichiometry | Guides students through complex calculations step-by-step using only guiding questions. | [View Prompt](/projectsgit/ai-in-education/docs/socratic_chemistry_tutor)                  | 
| **ELL Text Simplifier  & Vocabulary Scaffolder**          | Vocabulary / Reading | Takes a dense scientific paragraph and outputs a simplified version with a target vocabulary list. | [View Prompt](/projectsgit/ai-in-education/docs/ell_text_simplifier)  | 
| .. | .. | .. | .. |

## Part 2: Automated Build and Synchronization

Execute this single command from your Jekyll site root directory (mkahveci.github.io/) after making any remote changes.

**Full Workflow Command**

```bash
ruby _scripts/build_projects.rb
```

### Script Actions (Executed Sequentially)
1. Download & Clean (ReadmeDownloader):
   - Connects to GitHub and downloads the main README.md and all files within the docs/ folder for every listed project. 
   - Creates the necessary local folder structure (e.g., projectsgit/ai-in-education/docs/).
   - Handles GitHub caching issues and attempts to download the file directly if the API directory check fails.
   - Automatically creates the docs/index.html redirect page to handle manual URL lookups.
2. Preprocess Markdown (MarkdownPreprocessor):
    - Adds Front Matter: Scans all .md files (including new ones in docs/) and inserts the required YAML Front Matter (--- layout: projectgit ---).
    - Renames Index: Renames README.md to index.md for clean URLs.
    - Fixes Links: Converts all internal .md links to .html links, and converts source code links to direct GitHub URLs.
3. Generate Data (DataGenerator):
    - Connects to the GitHub API to fetch repository metadata (description, contributors, latest commit).
    - Writes all aggregated data to _data/projectsgit.yml, which powers your main project listing page.
4. Finalize: Once the script is complete, start your Jekyll server.

```bash
jekyll serve
```

## Part 3: Custom Prompt Template

Use this template as the base for all new Markdown prompt files you place in your docs/ folder.

```markdown
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
```