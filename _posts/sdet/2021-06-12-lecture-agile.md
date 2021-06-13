---
title: "Lecture: Agile"
author: Murat Kahveci
excerpt: 
summary: Lecture notes of 6/12/2021 meeting. Agile.
tags: [sdet,agile]
sidebar: sdet_sidebar
permalink: vtt.html
published: true  
---

## 1 Review on Testing

FrontEnd / User Interface

Backend
* Database
* API

Static testing: test doc

* SRC: business team & clients
* SDS: designers, the client, PM
* test plan > testers

#### For example: A scenario

As a user, I want to upload files so that I can share with others.

Assign to a developer:

* unit 1: file upload to an individual person
* unit 2: file upload to a channel
* unit 3: file saved in database
* unit 4: file upload with API

Unit test: developers test their code. One individual small unit is tested.

{% include note.html content="Although SDET / QA know how to write code unit by unit, use unit test tool like Junit/testNG, but SDET's testing is not called unit test." %}

Same user story will assign to an Agile tester:
* frontEnd file upload: business scenarios
    * upload a new file
    * edit file name / info
    * delete file
    * send to an individual 
    * send to a channel
* database file upload
    * all the files do exist?
    * saved in correct location
* API file upload
    * Can I get a file from database to frontEnd?
* Nonfunctional/performance team responsibility?
    * How fast/slow?
    * Download speed?
    * Search result?
    * Volume?
    * Stress?

User Acceptance Test (UAT) - Alpha: real world scenarios

Po or BA provide real world scenarios, based on that, UAT team automate the app one more time.

#### For example: A scenario

* login
    * search a user/friend
    * send/upload a file
    * logout

One UAT tester will write code from login to logout in one file.
* End to end testing.


#### For example: A scenario

End to end scenarios for using Amazon in real world:
* login > search item > add to the cart > logout
* login > search item > got to the cart > make payment > history > logout


## 2 Review of Agile

* Next week 6/14 - 6/19: Java
* Upcoming week 6/21 - 6/26 Agile again, just recordings of people's real experience at work. And, some quizzes.

There are many project methodologies to choose for IT companies:
* Waterfall
    * Famous
    * Process is slow (disadvantage)
    * Not focused on anymore
* Agile
    * Famous
    * In US, 100% uses this methodology
* V-model
* etc (in total 7 types)

Project methodologies are decided at the company level. 

### 2.1 Waterfall

Coming from manufacturer industry. Rules:

* estimation 2 years
* entire project plan > release date: 6/23
* all the requirements


Advantages:

* easy to understand and implement
* easy to measure progress
* stability: project management is easy
* stages reduce the complexity
* quality and detailed documentation

Disadvantages:

* poor software result for long durations and large projects
* linear dependency
* little to no changes

### 2.2 Agile

4 values; 12 principles

