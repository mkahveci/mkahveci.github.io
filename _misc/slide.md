---
layout: misc
title: Code Snippets for Slides
date: 2025-11-16 00:00:00
permalink: /slide
---

This document contains a comprehensive guide to the code snippets for building your presentations using `Jekyll` and `reveal.js`. Use these [templates](/template) and notes to ensure consistency and proper rendering for every talk you create.

## 1. Front Matter

{% highlight yaml %}
{% raw %}

---
layout: reveal

# PRESENTATION METADATA (Used for site listing and slide)
title: "AI-Driven LT Tracker (5-SC)"
subtitle_desc: "Data-Driven Instructional Planning"
date: 2025-10-15
category: talks
event: "Professional Development Seminar"
location: "Chicago" # Used for slide footer and listing
type: "invited" # Use "conference" or "invited"

# ⭐ SLIDE CONFIGURATION
# Options: 'kahveci-light' (Default) or 'kahveci-dark'
presentation_theme: kahveci-dark

# 🎯 AUTHOR DATA (The array needed for _includes/title-slide.html)
authors:
- name: Murat Kahveci, Ph.D.
  affiliation: Chicago Public Schools
  photo: "/images/team/murat-kahveci.jpg"
  url: "/murat/"
# Add more authors as needed...

# FUNDING DATA
funding:
- "National Science Foundation"
# Add more funding as needed...


# ---- Optional Links for Buttons ----
pdf:
video:
event_url:
published: true
sitemap: false
---

{% endraw %}
{% endhighlight %}

## 2. Title Slide

This code generates your title slide with your custom branding. It uses a flexible `flexbox` layout for proper alignment.

{% highlight liquid %}
{% raw %}

{% include slide-title.html
    slide_title=page.title
    subtitle=page.subtitle_desc
    authors=page.authors
    location=page.location
    event=page.event
    date=page.date
    logo_src="/images/logo.svg"
%}

---

{% endraw %}
{% endhighlight %}

## 3. Content Slides
Use Markdown for your main content slides for simplicity. Separate each slide with ---.

### 3.1 Standard Slide

{% highlight markdown %}
{% raw %}

## 1. Introduction & Background

* Use bullet points for key concepts.
* Keep text concise and to the point.
* You can use **bold** or *italic* formatting for emphasis.

{% endraw %}
{% endhighlight %}

{% highlight markdown %}
{% raw %}

## 1. The Challenge: Reaching Every Learner

<div class="fragment" data-fragment-index="1">
    <p><strong>Differentiation is complex.</strong> Creating materials for multiple proficiency levels for every lesson is incredibly time-consuming.</p>
</div>

<div class="fragment" data-fragment-index="2">
    <p><strong>Language is a barrier.</strong> Scaffolding complex texts, scientific jargon, and abstract concepts for our ELLs is a daily struggle.</p>
</div>

{% endraw %}
{% endhighlight %}

---

### 3.2 Table

Use this template to add tables with a proper caption. The caption is now placed below the table for consistency with figures.

{% highlight liquid %}
{% raw %}

---

{% include slide-table-text.html
    title="s"
    headers="Col A,Col B"
    rows="Data 1|Data 2,Data 3|Data 4"
    caption=""
    text_items="Bullet point one; Bullet point two"
    table_align="left"
%}

---

{% endraw %}
{% endhighlight %}


### 3.3 Images and Figures

{% highlight liquid %}
{% raw %} 

---

{% include slide-figure-text.html
title=""
image_src="/images/talks/"
fig_num="1"
caption_title=""
caption_body=""
text_items="Bullet point one; Bullet point two"
image_align="right"
%}

---

{% endraw %}
{% endhighlight %}

### 3.4 Math Equations

You can embed \\(\LaTeX\\) math equations directly into your markdown.

**Equation Block**

{% highlight liquid %}
{% raw %}

$$\text{CFA} \ge 0.95$$

{% endraw %}
{% endhighlight %}

Will render as equation block, when placed as a new paragraph. 

$$\text{CFA} \ge 0.95$$

**In-line Equation**

{% highlight liquid %}
{% raw %}

\\(\text{CFA} \ge 0.95\\)

{% endraw %}
{% endhighlight %}

{% highlight liquid %}
{% raw %}

$$\text{CFA} \ge 0.95$$

{% endraw %}
{% endhighlight %}

Will render as inline equation: $$\text{CFA} \ge 0.95$$, when placed in-line.


## 4. End Slides

These final two slides are designed as HTML sections to ensure all your custom styling and icons render correctly.

### 4.1 Acknowledgments Slide

{% highlight liquid %}
{% raw %}

---

{% include slide-acknowledgments.html
funding=page.funding
authors=page.authors
%}

---

{% endraw %}
{% endhighlight %}

### 4.2 Thank You Slide
This slide uses a personal quote and your logo for a memorable and professional conclusion.

{% highlight liquid %}
{% raw %}

---

{% include slide-questions-discussion.html
    title="Questions & Discussion"
    subtitle="Thank you for attending!"
    presenter="Murat Kahveci, Ph.D."
%}

{% endraw %}
{% endhighlight %}

## 5. How to Add a Presentation URL to a Publication

To link a "Slides" button to your presentation, you need to add the `presentation_url` variable to the YAML front matter of the specific post or page file.

1.  **Navigate to the File:** Locate and open the Markdown file (`.md`) for the talk or publication that needs the presentation link.
2.  **Edit the Front Matter:** At the very top of the file, you will see a section enclosed by three dashes (`---`). This is the `YAML` front matter.
3.  **Add the URL Line:** Add the following line anywhere within that section:

{% highlight yaml %}
{% raw %}

presentation_url: /narst2015-stpd

{% endraw %}
{% endhighlight %}