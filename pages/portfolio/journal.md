---
title: Journal Articles Overview
keywords: publications, book, journal, conference
tags: [portfolio]
summary: This page presents the list of publications categorized as Journal Papers. More details for each publication can be found by following the link sign at the end. Alternatively, the navigation menu on the left has these categories, folded with respective titles. 
sidebar: portfolio_sidebar
permalink: journal.html
folder: portfolio
last_updated: Aug 30, 2020
---

{% assign count = 0 %}
{% 
    assign journals = site.pages 
    | sort:"year"
    | reverse
    | where_exp: "item", "item.journal == true" 
%} 

{% for journal in journals %}
{% assign count = count | plus: 1 %}
{% endfor %}

{% for page in journals %}
__{{ count }}__. {{page.ref }} <a class="noCrossRef" href="{{ site.urlx }}{{ page.url }}"><i class="fa fa-link"></i></a>
{% assign count = count | minus: 1 %}
{% endfor %}