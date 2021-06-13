---
title: Overview
sidebar: portfolio_sidebar
permalink: /index.html
# summary: Welcome to the academic portfolio of Kahveci Group. We are advocates of Chemistry Education Research (CER). 
redirect_from:
  - /pdf
  - /pdf/
toc: false
---

{% capture note_1 %}
If you're reading this webpage, you're probably a researcher in the field of chemistry education research (CER) or a student of mine. I have a <a alt='blog' href="{{ site.urlx }}/blog.html">blog</a> on both <a href="{{ site.urlx }}/project.html">research</a> and teaching. If you'd like to stay updated with the latest trends, best practices, and other methods for chemistry education research, consider <a href='https://tinyletter.com/mkahveci'>subscribing</a> our group's newsletter.
{% endcapture %}


<p style="font-size:20px">The Kahveci Group at the DePaul University works at the interface of affective dimensions
in chemistry education research. We apply quantitative research methods to analyze data and understand how learning complex chemistry topics is
influenced by affective variables. We are also studying diversity issues in chemistry education and gaining new insights on pure computational
chemistry research.</p>

{% include note.html content=note_1 %}

{% capture caption %}
With colleagues attending to the <a href="{{ site.urlx }}/rwo.html">21st Symposium on Chemical and Science Education</a>. TU Dortmund University, Dortmund, Germany. May 17-19, 2012.
{% endcapture %}

{% include image.html file="/portfolio/dortmund2012.jpg" caption=caption max-width="700" %}

## 1 Join

New ideas on joint research proposals and publications are welcome. We are eager to meet and collaborate with new researchers and research groups in the chemistry education domain.

## 2 Publishers

We are always eager to publish our studies to reach out wider community across the globe. We would be happy to talk with the publishers in the field for our research outlet.

## 3 Students

If you are in need of an external committee member for your Master's or doctoral research study, our group would be interested in discussing future possibilities.

Our group welcomes new members of undergraduate students, who are interested in chemistry education research. Learning chemistry is always exciting. Likewise, researching how people learn chemistry as patterns of preferences is equally interesting and exciting.

## 4 Team

{% 
    assign sorted_members = site.pages 
    | sort:"date"
    | where_exp: "item", "item.team == true" 
%}

<ul>
{% for member in sorted_members %}
  <li>
    {{member.title}}<br><i>{{member.position}}</i> <a class="noCrossRef" href="{{ site.urlx }}{{member.url}}"><i class="fa fa-link"></i></a>
  </li>
{% endfor %}  
</ul>

## 5 Latest

{% 
    assign sorted = site.pages 
    | sort:"year"
    | reverse
    | where_exp: "item", "item.book == true" 
%} 
{% for item in sorted limit:1 %}
  <ul>
    <li><i>Book.</i>&nbsp;&nbsp;{{item.title}} <a class="noCrossRef" href="{{ site.urlx }}{{ item.url }}"><i class="fa fa-link"></i></a></li>
  </ul>
{% endfor %}
{% 
    assign sorted = site.pages 
    | sort:"year"
    | reverse
    | where_exp: "item", "item.journal == true"
%} 
{% for item in sorted limit:1 %}
  <ul>
    <li><i>Journal Article.</i>&nbsp;&nbsp;{{item.title}} <a class="noCrossRef" href="{{ site.urlx }}{{ item.url }}"><i class="fa fa-link"></i></a></li>
  </ul>
{% endfor %}
{% 
    assign sorted = site.pages 
    | sort:"year"
    | reverse
    | where_exp: "item", "item.conference == true" 
%} 
{% for item in sorted limit:1 %}
  <ul>
    <li><i>Conference Paper.</i>&nbsp;&nbsp;{{item.title}} <a class="noCrossRef" href="{{ site.urlx }}{{ item.url }}"><i class="fa fa-link"></i></a></li>
  </ul>
{% endfor %
{% endfor %}

{% 
    assign sorted = site.posts 
    | sort:"date"
    | reverse
%} 
{% for item in sorted limit:1 %}
  <ul>
    <li><i>Post.</i>&nbsp;&nbsp;{{item.title}} <a class="noCrossRef" href="{{ site.urlx }}{{ item.url }}"><i class="fa fa-link"></i></a></li>
  </ul>
{% endfor %}


{% include links.html %}
