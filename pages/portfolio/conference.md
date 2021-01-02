---
title: Conference Papers Overview
tags: [portfolio]
summary: This page presents the list of publications categorized as Conference Papers. More details for each publication can be found by following the link sign at the end. Alternatively, the navigation menu on the left has these categories, folded with respective titles. 
sidebar: portfolio_sidebar
permalink: conference.html
folder: portfolio
last_updated: Aug 30, 2020
---

{% assign count = 0 %}
{% 
    assign conferences = site.pages 
    | sort:"year"
    | reverse
    | where_exp: "item", "item.conference == true" 
%} 

{% for cpaper in conferences %}
{% assign count = count | plus: 1 %}
{% endfor %}

{% for page in conferences %}
__{{ count }}__. {{page.ref }} <a class="noCrossRef" href="{{ site.urlx }}{{ page.url }}"><i class="fa fa-link"></i></a>
{% assign count = count | minus: 1 %}
{% endfor %}