---
layout: projectgit
title: "Option Trade Ideas"
project: qma
repo: mkahveci/qma
permalink: /:path/:basename:output_ext
---

<div class="container my-5">

  <div class="text-center mb-5">
    <p class="lead col-lg-8 mx-auto">
      A log of personal trade ideas based on market analysis, focusing on options premium selling strategies. This is for educational and entertainment purposes only.
    </p>
  </div>

{% comment %} --- LIQUID DATA ASSIGNMENT (Now trusts file order) --- {% endcomment %}
{% assign sorted_trades = site.data.trade_ideas %}

  <section id="trades">
    <h2 class="display-6 mb-4 mt-5"><i class="fas fa-chart-line fa-fw text-muted me-2"></i> Options Trading Log</h2>

    {% comment %} --- UPDATED FILTER: Show Last 10 (default) or Last 50 --- {% endcomment %}
    <div class="d-flex justify-content-end mb-4">
        <div class="limit-filter-container">
            <label for="limit-filter-selector" class="form-label d-none d-lg-inline-block small text-muted me-2 mb-0">Show Trades:</label>
            <select id="limit-filter-selector" class="form-select form-select-sm d-inline-block w-auto">
                <option value="10" selected>Last 10 Trades</option>
                <option value="50">Last 50 Trades</option>
            </select>
        </div>
    </div>
    
    <div class="row row-cols-1 g-4">
      {% assign trades_to_show = 50 %}
      {% assign current_count = 0 %}
      
      {% for trade in sorted_trades %}
      
          {% comment %} MANUAL LIMIT ENFORCEMENT: STOP AFTER 50 RECORDS {% endcomment %}
          {% if current_count >= trades_to_show %}
              {% break %}
          {% endif %}
          
          <div class="col trade-card-wrapper">
            <div class="card h-100 shadow-sm border-0 d-flex">
              <div class="card-body d-flex">

                <div class="date-block me-3">
                  <span class="month">{{ trade.publicationDate | date: "%b" | upcase }}</span>
                  <span class="day">{{ trade.publicationDate | date: "%d" }}</span>
                </div>
                
                <div class="flex-grow-1">

                  {% comment %} --- NEW STATUS LOGIC --- {% endcomment %}
                  {% assign last_step = trade.tradeProgression | last %}
                  {% if last_step and last_step.stepType == 'CLOSE' %}
                      {% assign trade_status = "CLOSED" %}
                  {% else %}
                      {% assign trade_status = "OPEN" %}
                  {% endif %}

                  <div class="trade-card-header">
                    <h5 class="card-title h6 mb-1">{{ trade.tradeTitle }}</h5>
                    {% if trade_status == "OPEN" %}
                      <span class="status-pill status-open">Open</span>
                    {% else %}
                      <span class="status-pill status-closed">Closed</span>
                    {% endif %}
                  </div>
                  
                  <p class="card-text small text-muted"><strong>Return:</strong> {{ trade.expectedReturnDisplay }}</p>

                  <div class="d-flex justify-content-between small p-2 rounded bg-light mt-2">
                    <span>Price: <strong>&#36;{%- capture price %}{% assign p = trade.currentPrice | to_s | split: '.' %}{{ p[0] }}.{% if p[1] == nil %}00{% elsif p[1].size == 1 %}{{ p[1] }}0{% else %}{{ p[1] | slice: 0, 2 }}{% endif %}{% endcapture %}{{ price | strip }}</strong></span>
                    <span>IV Rank: <strong>{{ trade.ivRank | default: "N/A" }}%</strong></span>
                    <span>Earnings: <strong>{{ trade.earningsDate | default: "N/A" }}</strong></span>
                  </div>
                  
                  <p class="card-text small mt-3">{{ trade.summaryJustification }}</p>

                  <div class="trade-card-section bg-light">
                    <ul class="list-unstyled small mb-0">
                      <li class="d-flex justify-content-between"><span><strong>Strategy:</strong></span><span class="font-monospace">{{ trade.analysis.strategyType }}</span></li>
                      <li class="d-flex justify-content-between pt-1"><span><strong>Expiration (DTE):</strong></span><span class="font-monospace">{{ trade.analysis.tradeDetails.expiration | date: "%b %d, %Y" }} ({{ trade.analysis.tradeDetails.dte }})</span></li>
                      <li class="d-flex justify-content-between pt-1"><span><strong>Net Credit:</strong></span><span class="font-monospace text-primary">&#36;{%- capture net_credit %}{% assign p = trade.analysis.tradeDetails.spreadDetails.netCredit | default: trade.analysis.tradeDetails.putPremium | to_s | split: '.' %}{{ p[0] }}.{% if p[1] == nil %}00{% elsif p[1].size == 1 %}{{ p[1] }}0{% else %}{{ p[1] | slice: 0, 2 }}{% endif %}{% endcapture %}{{ net_credit | strip }}</span></li>
                      <li class="d-flex justify-content-between pt-1"><span><strong>Max Profit:</strong></span><span class="font-monospace text-success">&#36;{%- capture max_profit %}{% assign p = trade.analysis.tradeDetails.maxProfit | to_s | split: '.' %}{{ p[0] }}.{% if p[1] == nil %}00{% elsif p[1].size == 1 %}{{ p[1] }}0{% else %}{{ p[1] | slice: 0, 2 }}{% endif %}{% endcapture %}{{ max_profit | strip }}</span></li>
                    </ul>
                    
                    <h6 class="small mt-3 mb-1"><strong>Leg Details</strong></h6>
                    <div class="leg-grid">
                      {% assign details = trade.analysis.tradeDetails.spreadDetails %}

                      {% if details.shortPutStrike > 0 %}
                      <div class="leg-item">
                        <strong>SELL PUT</strong>
                        <span class="text-danger">&#36;{{ details.shortPutStrike | round: 2 }}</span>
                      </div>
                      {% endif %}

                      {% if details.longPutStrike > 0 %}
                      <div class="leg-item">
                        <strong>BUY PUT</strong>
                        <span class="text-success">&#36;{{ details.longPutStrike | round: 2 }}</span>
                      </div>
                      {% endif %}

                      {% if details.shortCallStrike > 0 %}
                      <div class="leg-item">
                        <strong>SELL CALL</strong>
                        <span class="text-danger">&#36;{{ details.shortCallStrike | round: 2 }}</span>
                      </div>
                      {% endif %}

                      {% if details.longCallStrike > 0 %}
                      <div class="leg-item">
                        <strong>BUY CALL</strong>
                        <span class="text-success">&#36;{{ details.longCallStrike | round: 2 }}</span>
                      </div>
                      {% endif %}
                    </div>
                    </div>
                  <div class="trade-card-section" style="background-color: #f0f8ff;">
                    <div class="metrics-grid">
                      <div class="metric-item text-center"><strong>ROC</strong><span>{{ trade.analysis.metrics.roc | round: 2 }}%</span></div>
                      <div class="metric-item text-center"><strong>Annualized</strong><span>{{ trade.analysis.metrics.annualizedRoc | round: 2 }}%</span></div>
                      <div class="metric-item text-center"><strong>POP</strong><span>{{ trade.analysis.metrics.pop | round: 1 }}%</span></div>
                      <div class="metric-item text-center"><strong>Buying Power</strong><span>&#36;{{ trade.analysis.metrics.buyingPowerEffect | round: 0 }}</span></div>
                    </div>
                  </div>
                  
                  <div class="trade-progression-container small">
                    <h6 class="h6 small"><strong>Trade Progression Log</strong></h6>
                    
                    {% if trade.tradeProgression and trade.tradeProgression.size > 0 %}
                        <ol class="progression-timeline">
                            {% for step in trade.tradeProgression %}
                                {% assign step_type_lower = step.stepType | downcase %}
                                <li class="progression-step step-{{ step_type_lower }}">
                                    <div class="progression-header">
                                        <span class="progression-tag tag-{{ step_type_lower }}">{{ step.stepType }}</span>
                                        {% comment %} Adjusted for progression date DTE which uses 'dteRemaining' for CLOSE/ADJUST {% endcomment %}
                                        <span class="progression-date">{{ step.date | date: "%b %d, %Y" }} ({{ step.dteRemaining | default: trade.analysis.tradeDetails.dte }} DTE)</span>
                                    </div>
                                    <div class="progression-details">
                                        
                                        {% if step.stepType == 'OPEN' %}
                                            <p>{{ trade.summaryJustification }}</p>
                                            <span class="profit-loss text-primary">(+&#36;{{ trade.analysis.tradeDetails.spreadDetails.netCredit | default: trade.analysis.tradeDetails.putPremium | round: 2 }})</span>
                                        {% elsif step.stepType == 'ADJUSTMENT' %}
                                            <p>{{ step.description }}</p>
                                            <span class="profit-loss text-warning">(+&#36;{{ step.netCreditReceived | round: 2 }})</span>
                                            {% if step.managementRuleTrigger %}
                                              <p class="small text-muted mb-0 mt-1"><em>Trigger: {{ step.managementRuleTrigger }}</em></p>
                                            {% endif %}
                                        {% elsif step.stepType == 'CLOSE' %}
                                            {% comment %}
                                            *** CORRECTED CLOSE LOGIC START ***
                                            Accessing grossProfitLoss and transaction details directly from the step object.
                                            {% endcomment %}
                                            
                                            <span class="profit-loss">
                                                {% if step.grossProfitLoss >= 0 %}
                                                    <span class="text-success">(Profit: &#36;{{ step.grossProfitLoss | round: 2 }})</span>
                                                {% else %}
                                                    <span class="text-danger">(Loss: &#36;{{ step.grossProfitLoss | abs | round: 2 }})</span>
                                                {% endif %}
                                            </span>
                                            
                                            <p class="small text-muted mb-0 mt-1">
                                              Transaction: 
                                              {% if step.debitPaid and step.debitPaid > 0 %}
                                                <strong class="text-danger">Debit Paid &#36;{{ step.debitPaid | round: 2 }}</strong>
                                              {% elsif step.creditReceived and step.creditReceived > 0 %}
                                                <strong class="text-success">Credit Received &#36;{{ step.creditReceived | round: 2 }}</strong>
                                              {% endif %}
                                              <span class="ms-2">({{ step.actionTaken }})</span>
                                            </p>
                                            
                                            {% if step.notes %}
                                                <p class="small text-muted mb-0 mt-1"><em>{{ step.notes }}</em></p>
                                            {% endif %}
                                            
                                        {% endif %}
                                    </div>
                                </li>
                            {% endfor %}
                        </ol>
                    {% else %}
                        <p class="small text-muted mt-2 mb-0">No management steps recorded yet.</p>
                    {% endif %}
                  </div>
                  
                </div>
              </div>
              
              <div class="card-footer bg-white">
                <div class="d-flex flex-wrap justify-content-end" style="gap: 0.5rem;">
                  <a href="https://www.google.com/search?q={{ trade.ticker }}+stock" target="_blank" rel="noopener noreferrer" class="btn btn-sm btn-outline-primary"><i class="fas fa-chart-line fa-fw me-1"></i> Chart</a>
                  <button class="btn btn-sm btn-outline-info" type="button" data-bs-toggle="collapse" data-bs-target="#collapse-{{ current_count }}" aria-expanded="false" aria-controls="collapse-{{ current_count }}">
                    <i class="fas fa-info-circle fa-fw me-1"></i> Thesis & Plan
                  </button>
                  <button onclick="copyTradeDetails(this)" class="btn btn-sm btn-outline-secondary" title="Copy trade details"><i class="fas fa-copy fa-fw me-1"></i> Copy</button>

                  <div class="trade-details-data" style="display: none;">
                    Trade: {{ trade.tradeTitle }}
                    Strategy: {{ trade.analysis.strategyType }} ({{ trade.analysis.tradeDetails.dte }} DTE)
                    Expiration: {{ trade.analysis.tradeDetails.expiration | date: "%b %d" }}
                    {% if trade.analysis.tradeDetails.spreadDetails %}
                    Short Put: &#36;{{ trade.analysis.tradeDetails.spreadDetails.shortPutStrike | round: 2 }}
                    Long Put: &#36;{{ trade.analysis.tradeDetails.spreadDetails.longPutStrike | round: 2 }}
                    Short Call: &#36;{{ trade.analysis.tradeDetails.spreadDetails.shortCallStrike | round: 2 }}
                    Long Call: &#36;{{ trade.analysis.tradeDetails.spreadDetails.longCallStrike | round: 2 }}
                    Net Credit: &#36;{{ trade.analysis.tradeDetails.spreadDetails.netCredit | round: 2 }}
                    Max Profit: &#36;{{ trade.analysis.tradeDetails.maxProfit | round: 2 }}
                    {% else %}
                    Strike/Premium: &#36;{{ trade.analysis.tradeDetails.putStrike | round: 2 }} / &#36;{{ trade.analysis.tradeDetails.putPremium | round: 2 }}
                    Max Profit: &#36;{{ trade.analysis.tradeDetails.maxProfit | round: 2 }}
                    {% endif %}
                    ROC: {{ trade.analysis.metrics.roc | round: 2 }}%
                    Buying Power: &#36;{{ trade.analysis.metrics.buyingPowerEffect | round: 0 }}
                    POP: {{ trade.analysis.metrics.pop | round: 1 }}%
                  </div>
                </div>
                
                <div class="collapse mt-3" id="collapse-{{ current_count }}">
                  <div class="small p-3 rounded" style="background-color: #fffbe6;">
                    <h6 class="h6 small"><strong>Thesis</strong></h6>
                    <p>{{ trade.analysis.thesis }}</p>
                    <h6 classs="h6 small mt-3"><strong>Management Plan</strong></h6>
                    <p class="mb-0">{{ trade.analysis.managementPlan }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          {% assign current_count = current_count | plus: 1 %}
      {% endfor %}
    </div>
  </section>
</div>

<script>
    document.addEventListener('DOMContentLoaded', function() {
        const selector = document.getElementById('limit-filter-selector');
        const tradeCards = document.querySelectorAll('.trade-card-wrapper');

        function filterTrades(limit) {
            const numLimit = parseInt(limit);
            
            tradeCards.forEach((card, index) => {
                if (index < numLimit) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        }

        if (selector) {
            filterTrades(selector.value); 
            selector.addEventListener('change', function() {
                filterTrades(this.value);
            });
        }
    });
</script>
<script>
  function copyTradeDetails(button) {
    const detailsContainer = button.nextElementSibling; 
    const detailsText = detailsContainer.textContent.trim().replace(/\s+/g, ' ');

    navigator.clipboard.writeText(detailsText).then(() => {
      const originalIcon = button.innerHTML;
      button.innerHTML = '<i class="fas fa-check fa-fw me-1"></i> Copied!';
      button.classList.replace('btn-outline-secondary', 'btn-success');
      
      setTimeout(() => {
        button.innerHTML = originalIcon;
        button.classList.replace('btn-success', 'btn-outline-secondary');
      }, 2000);
    }).catch(err => {
      console.error('Failed to copy text: ', err);
    });
  }
</script>