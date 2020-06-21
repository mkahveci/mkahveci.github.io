---
layout: articles
title: Alumni
header:
  theme: dark
  background: 'linear-gradient(135deg, rgb(34, 139, 87), rgb(139, 34, 139))'
articles:
  data_source: site.team_alumni
  cover_size: sm
  show_excerpt: true
  excerpt_type: html
  show_readmore: true
  show_info: true
sidebar:
  nav: team   
---

Number of alumni: {{ site.team_alumni.size }}

{% include image.html
max-width="100%" file="https://source.unsplash.com/DNkoNXQti3c/1920x2898" alt="group"
caption="Image Credit: [Shane Rounce](https://unsplash.com/@shanerounce)" %}