---
layout: projectgit
title: learning-target-tracker-5sc
project: ai-in-education
repo: mkahveci/ai-in-education
permalink: /:path/:basename:output_ext
---

<div class="container my-5">
    <header class="mb-5 border-bottom pb-3">
        <h1 class="display-4 text-primary">The LT Tracker (5-SC)</h1>
        <p class="lead">A specialized, error-proof Learning Target tracking system built on Google Sheets for the AI-in-Education project.</p>
    </header>

    <section class="mb-5">
        <h2 class="h3 mb-3 text-secondary">Overview and Core Design</h2>
        <p>This system is built around a single, reusable template file that you can copy for each new <strong>Learning Target</strong>. It features automated reporting and is designed for fast, error-proof data entry on both desktop and mobile devices.</p>
        <p>For student privacy, the tracker is designed to work with either student names or anonymous <strong>Student IDs</strong>. Simply choose which identifier to use in your data entry and dashboard tabs to generate either standard or confidential reports.</p>
        
        <hr class="my-4">

        <h3 class="h4 mb-3 text-secondary">How the LT Status is Determined Automatically</h3>
        <p>The <strong>LT Status</strong> column provides a summative judgment on whether a student has mastered the overall Learning Target. It is calculated automatically based on a flexible, data-driven rule.</p>
        
        <blockquote class="blockquote border-start border-primary border-5 ps-3 py-2 bg-light rounded">
            <p class="mb-0 small text-dark fst-italic"><strong>The current rule is:</strong> A student has “<span class="text-success">✅ Met</span>” the Learning Target if the percentage of their graded Success Criteria marked as <strong>High</strong> or <strong>Expected</strong> is 80% or more.</p>
        </blockquote>

        <p>The formula automatically performs these three steps:</p>
        <ol>
            <li>Counts the total number of Success Criteria you’ve graded for a student.</li>
            <li>Counts how many of those grades are <strong>High</strong> or <strong>Expected</strong>.</li>
            <li>Calculates the percentage of success based only on the graded work.</li>
            <li>Compares that percentage to the 80% threshold and displays the final status.</li>
        </ol>
    </section>

    <div class="mt-5">
        <h2 class="h3 mb-4 text-secondary"><i class="fas fa-link me-2"></i> Key Resources</h2>
        <div class="row">
            <div class="col-12 col-md-8 col-lg-6"> 
                <div class="card shadow-sm bg-light">
                    <div class="card-body">
                        <ul class="list-unstyled g-3">
                            {% assign links = site.data.lt_tracker_links %}
                            {% for item in links %}
                            <li class="mb-3">
                                <div class="card h-100 border-0 p-2 bg-white d-flex flex-row align-items-center">
                                    <div class="text-center me-3" style="min-width: 50px;">
                                        <span class="h5 text-primary"><i class="{{ item.icon }}"></i></span>
                                    </div>
                                    <div class="flex-grow-1">
                                        <a href="{{ item.url }}" target="_blank" rel="noopener noreferrer" class="stretched-link text-decoration-none">
                                            <h6 class="mb-0 text-dark">{{ item.title }}</h6>
                                            <small class="text-muted">{{ item.description }}</small>
                                        </a>
                                    </div>
                                </div>
                            </li>
                            {% endfor %}
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>