---
layout: projectgit
title: "Option Trade Ideas"
project: qma
repo: mkahveci/qma
permalink: /:path/:basename:output_ext
---

<style>
  /* Style for the date block on the left of each card */
  .date-block {
    width: 70px;
    height: 70px;
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background-color: #f8f9fa;
    color: #495057;
    font-weight: bold;
    border-radius: 0.375rem;
    text-align: center;
    line-height: 1.2;
    border: 1px solid #dee2e6;
  }
  .date-block .month {
    font-size: 0.9rem;
    display: block;
  }
  .date-block .day {
    font-size: 1.6rem;
    display: block;
  }
  .trade-card-section {
    padding: 0.75rem;
    border-radius: 0.25rem;
    margin-top: 0.75rem;
  }
  .metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: 0.5rem;
    font-size: 0.8rem;
  }
  .metric-item {
    padding: 0.25rem 0.5rem;
    background-color: #fff;
    border-radius: 0.25rem;
    border: 1px solid #e9ecef;
  }
  .metric-item strong {
    display: block;
    color: #6c757d;
    font-size: 0.75rem;
  }
  .font-monospace {
      font-size: 0.9em;
  }
  .leg-details {
    margin-top: 0.5rem;
    padding-left: 0.5rem;
    border-left: 2px solid #007bff;
  }
</style>

<div class="container my-5">

  <div class="text-center mb-5">
    <p class="lead col-lg-8 mx-auto">
      A log of personal trade ideas based on market analysis, focusing on options premium selling strategies. This is for educational and entertainment purposes only.
    </p>
  </div>

{% assign sorted_trades = site.data.trade_ideas | sort: 'publicationDate' | reverse | limit: 100 %}

  <section id="trades">
    <h2 class="display-6 mb-4 mt-5"><i class="fas fa-chart-line fa-fw text-muted me-2"></i> Options Trading Log</h2>
    <div class="row row-cols-1 g-4">
      {% for trade in sorted_trades %}
      <div class="col">
        <div class="card h-100 shadow-sm border-0 d-flex">
          <div class="card-body d-flex">

            <div class="date-block me-3">
              <span class="month">{{ trade.publicationDate | date: "%b" | upcase }}</span>
              <span class="day">{{ trade.publicationDate | date: "%d" }}</span>
            </div>
            
            <div class="flex-grow-1">
              <h5 class="card-title h6 mb-1">{{ trade.tradeTitle }}</h5>
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
                <div class="leg-details">
                    {% if trade.analysis.tradeDetails.spreadDetails %}
                        <ul class="list-unstyled small mb-0">
                            <li class="pt-1">Sell Put: <strong>&#36;{{ trade.analysis.tradeDetails.spreadDetails.shortPutStrike | round: 2 }}</strong></li>
                            <li class="pt-1">Buy Put: <strong>&#36;{{ trade.analysis.tradeDetails.spreadDetails.longPutStrike | round: 2 }}</strong></li>
                            <li class="pt-1">Sell Call: <strong>&#36;{{ trade.analysis.tradeDetails.spreadDetails.shortCallStrike | round: 2 }}</strong></li>
                            <li class="pt-1">Buy Call: <strong>&#36;{{ trade.analysis.tradeDetails.spreadDetails.longCallStrike | round: 2 }}</strong></li>
                        </ul>
                    {% elsif trade.analysis.tradeDetails.putStrike %}
                        <ul class="list-unstyled small mb-0">
                            <li class="pt-1">Sell Put: <strong>&#36;{{ trade.analysis.tradeDetails.putStrike | round: 2 }}</strong> (Premium: &#36;{{ trade.analysis.tradeDetails.putPremium | round: 2 }})</li>
                        </ul>
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
              
            </div>
          </div>
          <div class="card-footer bg-white">
            <div class="d-flex flex-wrap justify-content-end" style="gap: 0.5rem;">
              <a href="https://www.google.com/search?q={{ trade.ticker }}+stock" target="_blank" rel="noopener noreferrer" class="btn btn-sm btn-outline-primary"><i class="fas fa-chart-line fa-fw me-1"></i> Chart</a>
              <button class="btn btn-sm btn-outline-info" type="button" data-bs-toggle="collapse" data-bs-target="#collapse-{{ forloop.index }}" aria-expanded="false" aria-controls="collapse-{{ forloop.index }}">
                <i class="fas fa-info-circle fa-fw me-1"></i> More Info
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
            
            <div class="collapse mt-3" id="collapse-{{ forloop.index }}">
              <div class="small p-3 rounded" style="background-color: #fffbe6;">
                <h6 class="h6 small"><strong>Thesis</strong></h6>
                <p>{{ trade.analysis.thesis }}</p>
                <h6 class="h6 small mt-3"><strong>Management Plan</strong></h6>
                <p class="mb-0">{{ trade.analysis.managementPlan }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      {% endfor %}
    </div>
  </section>
</div>

<script>
  function copyTradeDetails(button) {
    // Correctly selects the next sibling element which holds the data
    const detailsContainer = button.nextElementSibling; 
    // Normalize whitespace and replace multiple spaces with a single space
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