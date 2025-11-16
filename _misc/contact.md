---
layout: misc
title: Contact
date: 2022-08-19 00:00:00
---
<div class="container my-5">

    <div class="row justify-content-center">
        <div class="col-lg-8">

            {% comment %} The main card structure now uses the theme-aware background {% endcomment %}
            <div class="contact-card shadow-lg rounded-lg p-5" style="background-color: var(--bs-card-bg);">

                <h1 class="bigtitle text-center text-body">Murat Kahveci, Ph.D.</h1>
                <p class="text-center text-muted lead">
                    Feel free to get in touch regarding <b>academic collaborations</b>, reference requests, or inquiries about my work in chemistry education and EdTech innovation.
                </p>

                <div class="text-center mb-4">
                    
                    <img width="150" class="mb-3 rounded-circle border shadow" src="/images/team/murat-kahveci.jpg" alt="Murat Kahveci, Ph.D.">

                    <p class="mt-3">
                        <i class="fas fa-graduation-cap fa-fw text-primary"></i> <span class="text-body"><i>Instructor of Chemistry</i></span><br>
                        <i class="fas fa-map-marker-alt fa-fw text-primary"></i> 
                        <a href="https://www.cps.edu/" target="_blank" class="text-primary text-decoration-none">Chicago Public Schools</a>, <span class="text-muted">Chicago, IL 60602</span>
                    </p>

                    <div class="d-flex justify-content-center flex-wrap gap-3 mt-4">
                        {% comment %} Secondary buttons use btn-primary for high-contrast visibility {% endcomment %}
                        <a href="/murat" class="btn btn-lg btn-primary shadow-sm">
                            <i class="fas fa-user-graduate fa-fw"></i> Curriculum Vitae
                        </a>
                        <a href="/reference" class="btn btn-lg btn-primary shadow-sm">
                            <i class="fas fa-file-alt fa-fw"></i> Letter Request
                        </a>
                        <a href="https://calendar.app.google/9nEdwgNRgCiQ1HxaA" class="btn btn-lg btn-primary shadow-sm" target="_blank" rel="noopener noreferrer">
                            <i class="fas fa-calendar-alt fa-fw"></i> Schedule Meeting
                        </a>
                    </div>
                </div>

                <hr class="my-5" style="border-color: var(--bs-border-color);">

                <h3 class="head fw-bold text-center mb-4 text-primary">Direct Contact Information</h3>
                
                {% comment %} Direct Contact Card: Simplified to high-contrast dark box {% endcomment %}
                <div class="card shadow-sm border-0" style="background-color: var(--bs-tertiary-bg);">
                    <div class="card-body text-center py-4">
                        
                        <h4 class="mb-3 text-body">
                            <i class="fas fa-envelope fa-fw text-primary"></i> 
                            {% comment %} Email link uses mandated text-primary style {% endcomment %}
                            <a href="mailto:mkahveci@gmail.com" class="text-primary text-decoration-none">
                                <span>mkahveci</span>@gmail.com
                            </a>
                        </h4>

                        <h5 class="mb-0 text-body">
                            <i class="fas fa-phone fa-fw text-primary"></i> 
                            {% comment %} Phone link uses mandated text-primary style {% endcomment %}
                            <a href="tel:+17735355400" class="text-primary text-decoration-none">(773) 535-5400</a>
                        </h5>

                    </div>
                </div>

            </div>
        </div>
    </div>
</div>