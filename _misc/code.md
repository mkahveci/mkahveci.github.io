---
layout: misc
title: Code Snippets
date: 2013-10-28 00:00:00
permalink: /code
mermaid: true
---

### Page Redirect

{% highlight yaml %}
{% raw %}
redirect_from:
- /projectsgit/ai-in-education/
{% endraw %}
{% endhighlight %}
- 
### Related Protects Call Out

{% highlight yaml %}
{% raw %}
related_project:
  name: "Quantitative Market Analysis (qma)"
  url: /projectsgit/qma/
{% endraw %}
{% endhighlight %}

### Universal Figure Include (Image & Flowchart)

This single include can render either a **standard image** or a **Mermaid flowchart**, complete with automatic figure numbering (requires `figure_counter: 0` in the front matter).

{% highlight liquid %}
{% raw %}
{% include figure.html
image_url='/images/blog/latex.jpg'
image_alt='Description of chart data.'
caption='This figure shows market volatility over three quarters.'
%}
{% endraw %}
{% endhighlight %}

{% include figure.html
image_url='/images/blog/latex.jpg'
image_alt='The LaTeX Project logo.'
caption='1: \(\LaTeX\) for fun!'
%}

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

{% include figure.html
mermaid_code='graph LR
A[Start] --> B(Process);
B --> C{Decision?};'
caption='2: Simple Validation Flowchart (Left to Right Progression).'
%}

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

{% include figure.html
mermaid_code='graph TD
A[Start] --> B(Process);
B --> C{Decision?};'
caption='3: Simple Validation Flowchart (Top-Down Process View).'
%}

### Basic Callout Usage

Callouts are used to visually break up content and draw attention to important information. They use Bootstrap's **d-flex** layout for a clean, two-column look (Icon on the left, content on the right) and adhere to the site's professional pastel aesthetic.

{% highlight liquid %}
{% raw %}
{% include callout.html
  type="alert"
  title='Publications Entry Alert'
  content="Always verify collaborator search terms are in Last Name + Initial format (e.g., 'Kahveci M') for Publications/Projects filtering."
%}
{% endraw %}
{% endhighlight %}

{% include callout.html
type="alert"
title="Publications Entry Alert"
content="Always verify collaborator search terms are in Last Name + Initial format (e.g., 'Kahveci M') for Publications/Projects filtering."
%}

**Parameters**

* `type`: **(Required)** Controls the color and icon. See available options below.
* `title`: **(Required)** The `h5` heading inside the callout.
* `content`: **(Required)** The body text.

**Available Types**

| Type | Appearance | Icon |
| :--- | :--- | :--- |
| `note` | Primary, neutral information. | <i class="fas fa-sticky-note"></i> |
| `info` | Detailed guidance or official data. | <i class="fas fa-info-circle"></i> |
| `tip` | Best practice or helpful suggestion. | <i class="fas fa-lightbulb"></i> |
| `warning` | Non-critical caution. | <i class="fas fa-exclamation-triangle"></i> |
| `alert` | Critical requirement or error. | <i class="fas fa-exclamation-circle"></i> |


## Buttons

{% highlight html %}
{% raw %}
<a href="/contact" class="btn btn-outline-primary"><i class="fas fa-envelope"></i> Contact</a>
<a href="/murat" class="btn btn-outline-secondary"><i class="fas fa-user-graduate"></i> Dr. Kahveci</a>
{% endraw %}
{% endhighlight %}

<a href="/contact" class="btn btn-outline-primary"><i class="fas fa-envelope"></i> Contact</a>
<a href="/murat" class="btn btn-outline-secondary"><i class="fas fa-user-graduate"></i> Dr. Kahveci</a>

## Adding an Image

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

{% include image.html
file="/images/blog/latex.jpg"
title="Figure 1."
caption="Additional
caption text."
width="150px"
%}

## List relevant posts by a tag

{% highlight ruby %}
{% raw %}
{% include list-relevant-posts.html tag="LaTeX Tweaks" %}
{% endraw %}
{% endhighlight %}

{% include list-relevant-posts.html tag="LaTeX Tweaks" %}

<a href="/blog/tags/" class="btn btn-outline-secondary">Available Tags</a>

## Icon links (the photo links):

- **Journal Articles**: A deep blue like #0062B3 to signify academia and depth.

{% highlight liquid %}
{% raw %}
https://placehold.co/96x96/0062B3/ffffff?text=\n
{% endraw %}
{% endhighlight %}

 - **Books**: A classic maroon like #800000 for a scholarly and traditional feel.

{% highlight liquid %}
{% raw %}
https://placehold.co/96x96/800000/ffffff?text=\n
{% endraw %}
{% endhighlight %}

 - **Conferences**: A rich purple like #6A0DAD to suggest prestige and formality.

{% highlight liquid %}
{% raw %}
https://placehold.co/96x96/6A0DAD/ffffff?text=\n
{% endraw %}
{% endhighlight %}

 - **Talks**: A modern teal like #008080 for a fresh, engaging look.

{% highlight liquid %}
{% raw %}
https://placehold.co/96x96/008080/ffffff?text=\n
{% endraw %}
{% endhighlight %}

 - **Projects**: A professional green like #006400 to represent growth and progress.

{% highlight liquid %} 
{% raw %}
https://placehold.co/96x96/006400/ffffff?text=\n
{% endraw %}
{% endhighlight %}

 - **Courses**: A vibrant orange like #FF4500 to convey energy and creativity.

{% highlight liquid %}
{% raw %}
https://placehold.co/96x96/FF4500/ffffff?text=\n
{% endraw %}
{% endhighlight %}

## Embed a PDF file

{% highlight ruby %}
{% raw %}
{% include pdf.html pdf_file="/pdfs/eu/FP7-SiS-2008-1-call.pdf" %}
{% endraw %}
{% endhighlight %}

{% include pdf.html pdf_file="/pdfs/eu/FP7-SiS-2008-1-call.pdf" %}
