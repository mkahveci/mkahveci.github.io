---
title: Team Overview
keywords: team
tags: [portfolio]
sidebar: portfolio_sidebar
permalink: /team.html
summary: List of our group members including the alumni. Each contributing member has a short biography page to navigate.
redirect_from:
  - /pdf
  - /pdf/
toc: false  
---

## Group Members

{% 
    assign sorted_members = site.pages 
    | sort:"date"
    | where_exp: "item", "item.team == true" 
%}

<table>
<thead>
  <tr>
    <th>Name</th>
    <th>Position</th>
    <th>Duration</th>
  </tr>
</thead>
<tbody>
{% for member in sorted_members %}
  <tr>
    <td><a class="noCrossRef" href="{{ site.urlx }}{{member.url}}">{{member.title}}</a></td>
    <td>{{member.position}}</td>
    <td>{{member.duration}}</td>
  </tr>
{% endfor %}  
</tbody>
</table>

## Alumni

{% 
    assign sorted_members = site.pages 
    | sort:"date"
    | where_exp: "item", "item.alumni == true" 
%}

<table>
<thead>
  <tr>
    <th>Name</th>
    <th>Position</th>
    <th>Duration</th>
  </tr>
</thead>
<tbody>
{% for member in sorted_members %}
  <tr>
    <td><a class="noCrossRef" href="{{ site.urlx }}{{member.url}}">{{member.title}}</a></td>
    <td>{{member.position}}</td>
    <td>{{member.duration}}</td>
  </tr>
{% endfor %}  
</tbody>
</table>

{% include links.html %}