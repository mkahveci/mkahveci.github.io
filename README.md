# kahveci group research

## Purpose

The Kahveci Group at <a class="off" href="https://www.luc.edu">Loyola University Chicago</a> works at the interface of affective dimensions
in chemistry education research. We apply quantitative research methods to analyze data and understand how learning complex chemistry topics is influenced by affective variables in relation to personal characteristics. Additionally, we are interested in studying dominant modalities of remote learning as an extension of the post pandemic influences on the practice of chemistry education.

If you're reading this webpage, you're probably a researcher in the field of chemistry education research (CER) or a student of mine. I have a [blog](/blog) on both [research](/projects) and [teaching](/courses). If you'd like to stay updated with the latest trends, best practices, and chemistry education research, please consider <a href='https://tinyletter.com/mkahveci'>subscribing</a> our group's newsletter.

## Source code

[kahveci.pw](https://kahveci.pw) is built based on the source code of [bedford.io](https://github.com/blab/blotter), which is freely available at the [GitHub](https://github.com/blab/blotter).  This repo is placed under the [MIT license](https://github.com/blab/blotter#license).

### 1. Build site

To build the website locally, clone the repo with:

```
git clone https://github.com/blab/blotter.git
```

Then install necessary Ruby dependencies by running `bundle install` from within the `blotter` directory.  After this, the site can be be built with:

```
bundle exec jekyll build
```

(If you are getting errors at this stage, it may be due to your version of `bundle`. Try `gem uninstall bundler` + `gem install bundler -v 1.13.1`.)

To view the site, run `bundle exec jekyll serve` and point a browser to `http://localhost:4000/`.  More information on Jekyll can be found [here](http://jekyllrb.com/).

To include projects, preprocessing scripts are necessary to clone project repos and update Jekyll metadata. This can be accomplished with:

```
ruby _scripts/update-and-preprocess.rb
```

Then `jekyll build` works as normal.

### 2. Contribute

Blog posts just require YAML top matter that looks something like:

```
---
layout: post
title: Newton Institute presentation
author: Trevor Bedford
link: http://www.newton.ac.uk/programmes/IDD/seminars/2013082213301.html
image: /images/blog/transmission.png
---
```

The `layout`, `title` and `author` tags are required, while `link` and `image` are optional.  Just save a Markdown file with this top matter as something like `blog/_posts/2013-08-27-newton-institute.md`, where `2013-08-27` is the date of the post and `newton-institute` is the short title.  This short title is used in the URL of the post, so this becomes `blog/newton-institute/`, so the short title should be long enough and unique enough not to cause conflicts with other posts.

### 3. For more information

* Look over the [metadata format guide](/format/)
* Look over the [Markdown style guide](/style/)