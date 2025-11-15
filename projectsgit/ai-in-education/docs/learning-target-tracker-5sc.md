---
layout: projectgit
title: learning-target-tracker-5sc
project: ai-in-education
repo: mkahveci/ai-in-education
permalink: /learning-target-tracker-5sc/
---

<div class="container my-5">
    <header class="mb-5 border-bottom pb-3">
        <h1 class="bigtitle">The LT Tracker (5-SC)</h1>
        <p class="lead text-body">A specialized, error-proof Learning Target tracking system built on Google Sheets for the AI-in-Education project.</p>
    </header>

    <section class="mb-5">
        <h2 class="head fw-bold">Overview and Core Design</h2>
        <p class="text-body">This system is built around a single, reusable template file that you can copy for each new **Learning Target**. It features automated reporting and is designed for fast, error-proof data entry on both desktop and mobile devices.</p>
        <p class="text-body">For student privacy, the tracker is designed to work with either student names or anonymous **Student IDs**. Simply choose which identifier to use in your data entry and dashboard tabs to generate either standard or confidential reports.</p>
        
        <hr class="my-4">

        <h3 class="h4 mb-3 fw-bold text-body">How the LT Status is Determined Automatically</h3>
        <p class="text-body">The **LT Status** column provides a summative judgment on whether a student has mastered the overall Learning Target. It is calculated automatically based on a flexible, data-driven rule.</p>
        
        <blockquote class="blockquote border-start border-primary border-5 ps-3 py-2" style="background-color: var(--bs-card-bg);">
            <p class="mb-0 small text-body fst-italic">**The current rule is:** A student has “<span class="text-success">✅ Met</span>” the Learning Target if the percentage of their graded Success Criteria marked as **High** or **Expected** is 80% or more.</p>
        </blockquote>

        <p class="text-body">The formula automatically performs these three steps:</p>
        <ol class="text-body">
            <li>Counts the total number of Success Criteria you’ve graded for a student.</li>
            <li>Counts how many of those grades are **High** or **Expected**.</li>
            <li>Calculates the percentage of success based only on the graded work.</li>
            <li>Compares that percentage to the 80% threshold and displays the final status.</li>
        </ol>
    </section>

    <div class="mt-5">
        <h2 class="head fw-bold"><i class="fas fa-link me-2 text-body"></i> Key Resources</h2>
        <div class="row row-cols-1 row-cols-lg-2 g-4">
            {% assign links = site.data.lt_tracker_links %}
            {% for item in links %}
            <div class="col">
                <div class="card shadow-sm h-100 border-0" style="background-color: var(--bs-card-bg);">
                    <div class="card-body">
                        <div class="d-flex flex-row align-items-center">
                            <div class="flex-shrink-0 me-3 text-center">
                                <span class="h5 text-primary"><i class="{{ item.icon }}"></i></span>
                            </div>
                            <div class="flex-grow-1">
                                <a href="{{ item.url }}" target="_blank" rel="noopener noreferrer" class="stretched-link text-primary text-decoration-none">
                                    <h5 class="h5 fw-bold text-body mb-1">{{ item.title }}</h5>
                                    <small class="text-muted">{{ item.description }}</small>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</div>