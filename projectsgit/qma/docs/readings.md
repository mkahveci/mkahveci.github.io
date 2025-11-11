---
layout: projectgit
title: "Readings & Documentation"
project: qma
permalink: /qma-readings/
---

<div class="container my-5">
    <header class="mb-5"> 
        <p class="lead">A curated list of blog posts and guides detailing the theoretical and practical trading strategies that underpin Quantitative Market Analysis (qma) project.</p> 
        <hr>
    </header>

    <section class="mb-5">
        <h2 class="h3 fw-normal mb-4">Core Trading Concepts</h2>
        
        <div class="row row-cols-1 row-cols-lg-2 g-4">
            
            {% assign sorted_readings = site.data.qma_readings | sort: 'date' | reverse %}
            {% for reading in sorted_readings %}
            <div class="col">
                <a href="{{ reading.link | relative_url }}" class="text-decoration-none">
                    <div class="card shadow-sm h-100 border-0" style="background-color: var(--bs-card-bg);">
                        <div class="card-body d-flex">
                            
                            <div class="me-3 text-primary" style="min-width: 50px;">
                                <i class="{{ reading.icon }} fa-3x"></i>
                            </div>
                            
                            <div>
                                <h5 class="card-title fw-bold text-body">{{ reading.title }}</h5>
                                <p class="card-text small text-muted mb-2">{{ reading.excerpt }}</p>
                                
                                <footer class="mt-2 border-top pt-2">
                                    <small class="text-secondary d-block">
                                        <i class="fas fa-calendar-alt me-1"></i> {{ reading.date | date: "%Y-%m-%d" }} 
                                        <span class="ms-3"><i class="fas fa-user me-1"></i> {{ reading.author }}</span>
                                    </small>
                                </footer>
                            </div>
                        </div>
                    </div>
                </a>
            </div>
            {% endfor %}
            
        </div>
    </section>

</div>