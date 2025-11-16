---
layout: misc
title: Automated Post Creation Script
date: 2024-12-14 00:00:00
---

I've developed a Python script, `permalink.py`, to streamline the process of creating new posts for various content types on {% include knx.html %} (papers, projects, courses, albums, and blog posts). This script automates several tasks:

1. **Permalink Management:**
  - Extracts existing permalinks from all Markdown files (`.md`) within the website's directory.
  - Stores the extracted permalinks in a file named `existing_permalinks.txt` in the `_plugins` directory.
  - Generates a new, unique permalink that is not already in use.

2. **Post Creation:**
  - Creates a new Markdown file for the specified post type in the appropriate directory (e.g., `papers/_posts`, `projects/_posts`, etc.).
  - Automatically generates the YAML front matter for the post, including the necessary fields for each post type (title, author, tags, etc.).
  - Includes placeholder content after the YAML front matter, tailored to each post type. For example, paper posts include placeholders for an abstract and keywords, while project posts have sections for a synopsis, acronym explanation, and project description.

3. **Directory Management:**
  - Ensures the necessary directories exist for each post type. If a directory is missing, the script creates it automatically.

**Usage:**

To use the script, follow these steps:

1. **Save the script:** Save the provided Python code as `permalink.py` in your website's root directory.
2. **Make it executable:** Open your terminal and navigate to the root directory. Then, run the command `chmod +x permalink.py` to make the script executable.
3. **Run the script:** To create a new post, use the following command in your terminal:

{% highlight bash %}
{% raw %}
python3 permalink.py <post_type>
{% endraw %}
{% endhighlight %}

Replace `<post_type>` with: `paper`, `project`, `course`, `album`, or `blog`.

Example:

{% highlight bash %}
{% raw %}
python3 permalink.py project
{% endraw %}
{% endhighlight %}

This command creates a new project post with a unique permalink and the following YAML front matter:

{% highlight YAML %}
{% raw %}
layout: project
title: "Enhancing General Chemistry Education through Innovative Pedagogical Approaches"
# ... other YAML fields ...
permalink: /xyz
{% endraw %}
{% endhighlight %}

And the following placeholder content:

{% highlight MarkDown %}
{% raw %}
## Synopsis

## Project Acronym

**EChEmpower**

**ECh**: Enhancing Chemistry
**Empower**: Signifies the empowerment of both educators and students...

## Project Description

1. **Background and Motivation**:

# ... other sections ...

### Conclusion

Conslusion here

{%- include project-contributions.html -%}
{% endraw %}
{% endhighlight %}

## YAML Front Matter and Placeholders:

The script supports different YAML fields and placeholders for each post type. Here's a summary:

### Paper:

* YAML fields: layout, title, image, authors, year, publisher, projectid, ref, pdf, rgpdf, doi, journal, permalink.
* Placeholders: Abstract, keywords, citation include.

### Project:

* YAML fields: layout, title, image, projectid, contributors, duration, year, publisher, position, hostedby, fundedby, budget, pdf, web, excerpt, project, permalink.
* Placeholders: Synopsis, acronym, description, conclusion, contributions include.

### Course:

* YAML fields: layout, image, code, title, instructor, instructorurl, institution, insturl, clevel, year, semester, pdf, web, published, permalink.
* Placeholders: Description, materials, grade distribution, scope and sequence, classroom policies, science safety agreement.

### Album:

* YAML fields: layout, title, image, author, place, published, permalink.
* No specific placeholders.

### Blog:

* YAML fields: layout, author, title, tags, permalink.
* No specific placeholders.

## Benefits:

* **Efficiency**: Automates repetitive tasks.
* **Consistency**: Ensures consistent YAML and file organization.
* **Accuracy**: Reduces errors.
* **Maintainability**: Provides a centralized script for managing post creation.