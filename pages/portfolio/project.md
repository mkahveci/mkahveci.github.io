---
title: Projects Overview
keywords: projects
tags: [portfolio]
last_updated: Aug 26, 2020
summary: This page presents the list of projects. More details for each project can be found by following the link sign at the end. Alternatively, the navigation menu on the top has these titles. 
sidebar: portfolio_sidebar
permalink: project.html
folder: portfolio
---

{% assign sorted = site.pages | sort: 'year' | reverse %}
 
<ul>

{% for page in sorted %}
{% if page.project %}
<li>{{ page.title }} <a class="noCrossRef" href="{{ site.urlx }}{{ page.url }}"><i class="fa fa-link"></i></a></li>
<ul>
  <li>{{ page.duration }}</li>
  <li>{{ page.position }}</li>
</ul>
{% endif %}
{% endfor %}
</ul>