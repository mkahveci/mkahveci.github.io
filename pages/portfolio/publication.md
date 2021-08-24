---
title: Publications Overview
keywords: sample homepage
tags: [portfolio]
sidebar: portfolio_sidebar
permalink: /publication.html
summary: This page presents the list of publication categories. More details for each category can be found by following the link sign at the end. Alternatively, the navigation menu on the left has these titles.
redirect_from:
  - /pdf
  - /pdf/
toc: false  
---

## Publication Categories

  <ul>
    <li><a class="noCrossRef" href="{{ site.urlx }}/book.html">Books</a></li>
{% 
    assign sorted = site.pages 
    | sort:"year"
    | reverse
    | where_exp: "item", "item.book == true" 
%} 
{% for item in sorted limit:1 %}
<ul>
    <li><i>Latest:</i> {{item.ref}} <a class="noCrossRef" href="{{ site.urlx }}{{item.url}}"><i class="fa fa-link"></i></a></li>
{% endfor %}
</ul>

<li><a class="noCrossRef" href="{{ site.urlx }}/journal.html">Journal Articles</a></li>

{% 
    assign sorted = site.pages 
    | sort:"year"
    | reverse
    | where_exp: "item", "item.journal == true" 
%} 
{% for item in sorted limit:1 %}
<ul>
    <li><i>Latest:</i> {{item.ref}} <a class="noCrossRef" href="{{ site.urlx }}{{item.url}}"><i class="fa fa-link"></i></a></li>
{% endfor %}
</ul>

<li><a class="noCrossRef" href="{{ site.urlx }}/conference.html">Conference Papers </a></li>
{% 
    assign sorted = site.pages 
    | sort:"year"
    | reverse
    | where_exp: "item", "item.conference == true" 
%} 
{% for item in sorted limit:1 %}
<ul>
    <li><i>Latest:</i> {{item.ref}} <a class="noCrossRef" href="{{ site.urlx }}{{item.url}}"><i class="fa fa-link"></i></a></li>
{% endfor %}
</ul>

<li><a class="noCrossRef" href="{{ site.urlx }}/news_archive.html">Blog Posts</a></li>

{% 
    assign sorted = site.posts 
    | sort:"date"
    | reverse
%} 

{% for item in sorted limit:1 %}
<ul>
    <li><i>Latest:</i> {{item.title}} <a class="noCrossRef" href="{{ site.urlx }}{{item.url}}"><i class="fa fa-link"></i></a></li>
{% endfor %}
</ul>
</ul>

{% include links.html %}