---
layout: article
title: Biking Activities
years:
  - 2020
  - 2019
  - 2018

header:
  theme: dark
  # background: 'linear-gradient(135deg, rgb(34, 139, 87), rgb(139, 34, 139))'     
mode: immersive
article_header:
  type: cover
  image:
    src: /images/album/muratbiking.jpg  
modify_date: 2020-07-23       
---

{% include biking-header.html title=include.title %}

```mermaid
graph TB;
    A[Am I cycling outdoor?]
    B[I share my stats below.]
    C[Is it road-bike only?]
    D[Are the activities GPS based?]
    E[Is Adidas Runtastic used?]
    F[Is watchOS Activity used?]
    G[Is Strava used?]
    A--yes-->B;
    A--yes-->C;
    C--yes-->B; 
    A--yes-->D; 
    D--yes-->B; 
    D--yes-->E;
    E--yes-->B;
    D--yes-->F;
    F--yes-->B;
    D--yes-->G;
    G--yes-->B;
```
{% include biking-stats-year-plot.html %}

## All Logs

{% include biking-stats-year-compact.html %}
