---
title: Books Overview
keywords: publications, book, journal, conference
tags: [portfolio]
last_updated: Aug 26, 2020
summary: This page presents the list of publications categorized as Books. More details for each publication can be found by following the link sign at the end. Alternatively, the navigation menu on the left has these categories, folded with respective titles. 
sidebar: portfolio_sidebar
permalink: book.html
folder: portfolio
series: "Book"
weight: 0
---

{% assign count = 0 %}
{% 
    assign books = site.pages 
    | sort:"year"
    | reverse
    | where_exp: "item", "item.book == true" 
%} 

{% for book in books %}
{% assign count = count | plus: 1 %}
{% endfor %}

{% for page in books %}
__{{ count }}__. {{page.ref }} <a class="noCrossRef" href="{{ site.urlx }}{{ page.url }}"><i class="fa fa-link"></i></a>
{% assign count = count | minus: 1 %}
{% endfor %}