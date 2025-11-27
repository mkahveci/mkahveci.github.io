---
layout: misc
title: Scaffold User Guide
date: 2025-11-27 12:00:00
permalink: /scaffold
---

This document is the central guide for creating all new content on this website. It details how to use the unified scaffolding script to automatically generate new, pre-filled posts for **projects, courses, blog posts, albums, and talks.**

The script streamlines the entire content creation process. It provides interactive prompts, handles automatic contributor linking, and generates the correct files and templates for each content type.

---

## 1. How to Use the Scaffolding Script

The `scaffold.py` script is a single, interactive tool that replaces all the old, separate `.sh` files. It will ask you what you want to create and then prompt you for all the necessary information.

### Step 1: Run the Script

From the root directory of the website, run the script (or the `new.sh` wrapper):

{% highlight bash %}
{% raw %}
./scaffold.py
{% endraw %}
{% endhighlight %}

### Step 2: Select a Post Type

You will see an interactive menu of all available post types.

{% highlight text %}
{% raw %}
Select a post type to create:
1.  Album
2.  Blog
3.  Course
4.  Project
5.  Talk
    Enter a number (1-5):
    {% endraw %}
    {% endhighlight %}

Type the number for the content you want to create (e.g., `1` for a new Album) and press Enter.

### Step 3: Answer the Prompts

The script will guide you through a series of prompts to gather the necessary data. This includes:

* **Titles & Excerpts:** Basic post information.
* **Contributors:** For `project` and `talk` posts, you will see a numbered list of all team members. You can select them in the correct order (e.g., `2, 1, 3`).
* **Media Loop (New):** For `album` posts, you will enter a loop to add multiple photos or videos interactively.

### Step 4: Get Your New File

Once you finish, the script will create the new file in the correct directory (e.g., `album/_posts/` or `projects/_posts/`) with the correct file extension (`.html` for talks, `.md` for everything else), ready for you to add your content.

---

## 2. How Contributor Linking Works

For `project` and `talk` posts, the script automatically generates links for the contributors you select. This system works by:

1.  **Scanning `team/_posts/`:** It reads all your team member `.md` files to get their names and filenames.
2.  **Using the `name` field:** The link text is pulled from the `name:` field in the team member's YAML (e.g., `name: Murat Kahveci`).
3.  **Using the `file_slug`:** The link URL is built from the file's slug to match your site's `/:title/` permalink structure.
    * `murat-kahveci.md` becomes `[Murat Kahveci](/murat-kahveci/)`
    * `2024-01-01-annemarie-kegler.md` becomes `[Annemarie Kegler](/annemarie-kegler/)`

---

## 3. Guide: `talk` Posts (Slides)

`talk` posts are saved as `.html` files in `talks/_posts/`. The script will prompt you for all the metadata needed for the title slide and automatically append the full slide deck template.

### 3.1 Front Matter (Generated)

{% highlight yaml %}
{% raw %}
---
layout: reveal
title: "AI-Driven LT Tracker (5-SC)"
subtitle_desc: "Data-Driven Instructional Planning"
date: 2025-10-15
category: talks
event: "Professional Development Seminar"
location: "Chicago"
type: "invited"
presentation_theme: kahveci-dark
authors:
- name: Murat Kahveci, Ph.D.
  affiliation: Chicago Public Schools
  photo: "/images/team/murat-kahveci.jpg"
  url: "/murat/"
  funding:
- "National Science Foundation"
---
{% endraw %}
{% endhighlight %}

*(Refer to previous documentation for slide-specific includes like tables, figures, and math).*

---

## 4. Guide: `project` Posts

`project` posts are saved as `.md` files in `projects/_posts/`.

**You will be prompted for:**

* **Title** & **Year**
* **Project ID:** A short slug (e.g., `pec-leap`).
* **Contributors:** A numbered list from `team/_posts`.
* **Duration:** (e.g., `2023 - 2024`).
* **Hosted/Funded By.**
* **Excerpt:** A one-sentence description.

---

## 5. Guide: `course` Posts

`course` posts are saved as `.md` files in `courses/_posts/`.

**You will be prompted for:**

* **Title** & **Year**
* **Course Code:** (e.g., `FSCI`).
* **Institution/URL.**
* **Levels/Semester.**

---

## 6. Guide: `blog` & `album` Posts

### Blog Posts
Saved in `blog/_posts/`. You will be prompted for **Title**, **Tags** (comma-separated), and **Excerpt**. Optionally, you can link a **Related Project**.

### Album Posts (Updated)
Saved in `album/_posts/`. The new structure supports a mixed grid of Photos and YouTube videos.

**1. Initial Prompts:**
* **Title:** The name of the album/event.
* **Place:** Location (e.g., "Cancún, Mexico").

**2. Interactive Media Loop:**
The script will ask: `Select type: [1] Image, [2] YouTube, [Enter] Finish`.

* **Option 1 (Image):**
    * Enter the local URL: `/assets/img/my-photo.jpg`
    * Enter a Caption.
* **Option 2 (YouTube):**
    * Enter the ID only: `dQw4w9WgXcQ` (The part after `v=`).
    * Enter a Title.
* **Finish:** Press Enter on a blank line to generate the file.

#### 📸 Image Optimization Guidelines
To ensure the unified grid (16:9 ratio) and the full-screen lightbox load quickly and look sharp, please adhere to these specs before uploading images to `assets/img/`.

| Feature | Target Spec | Reason |
|---|---|---|
| **Dimensions** | **Longest Side: 1600px** | **Landscape:** Set Width to 1600px.<br>**Portrait:** Set Height to 1600px.<br>This prevents vertical photos from becoming massive files. |
| **Grid Crop** | **16:9 Ratio** | The site's CSS automatically crops the top/bottom to force a clean, uniform grid. |
| **File Size** | **200KB – 400KB** | Ensures fast loading, especially on mobile networks. |
| **Format** | **.jpg** or **.webp** | Best compression for photos. Avoid .png. |

#### YAML Structure Reference
The script will generate the following structure in your front matter:

{% highlight yaml %}
{% raw %}
media:
- type: image
  url: /assets/img/cancun-beach.jpg
  caption: "A beautiful day."
- type: youtube
  id: "dQw4w9WgXcQ"
  title: "Jetski Video"
  {% endraw %}
  {% endhighlight %}

---

## 7. Linking Content

To link a "Slides" button from a publication or project page *to* a presentation, add the `presentation_url` variable to the YAML front matter of that specific post.

{% highlight yaml %}
{% raw %}
presentation_url: /xyz
{% endraw %}
{% endhighlight %}