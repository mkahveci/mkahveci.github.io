---
layout: articles
title: Team
header:
  theme: dark
  background: 'linear-gradient(135deg, rgb(34, 139, 87), rgb(139, 34, 139))'
articles:
  data_source: site.team_member
  cover_size: sm
  show_excerpt: true
  excerpt_type: html
  show_readmore: true
  show_info: true 
modify_date: 2020-06-20  
---

Number of active members: {{ site.team_member.size }}

{% include image.html
max-width="100%" file="/images/album/team.jpg" alt="group"
caption="Image Credit: [Matteo Vistocco](https://unsplash.com/@mrsunflower94)" %}