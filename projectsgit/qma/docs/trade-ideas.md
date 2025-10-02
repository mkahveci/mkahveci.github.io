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
    width: 65px;
    height: 65px;
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background-color: #e9ecef;
    color: #495057;
    font-weight: bold;
    border-radius: 0.25rem;
    text-align: center;
    line-height: 1.2;
  }
  .date-block .month {
    font-size: 0.9rem;
    display: block;
  }
  .date-block .day {
    font-size: 1.5rem;
    display: block;
  }
</style>

<div class="container my-5">

  <div class="text-center mb-5">
    <p class="lead col-lg-8 mx-auto">
      A log of personal trade ideas based on market analysis, focusing on options premium selling strategies. This is for educational and entertainment purposes only.
    </p>
  </div>

{% assign sorted_trades = site.data.trade_ideas | sort: 'publicationDate' | reverse %}

  <section id="trades">
    <h2 class="display-6 mb-4 mt-5"><i class="fas fa-chart-line fa-fw text-muted me-2"></i> Options Trading Log</h2>
    <div class="row row-cols-1 row-cols-lg-2 g-4">
      {% for trade in sorted_trades %}
      <div class="col">
        <div class="card h-100 shadow-sm">
          <div class="card-body d-flex">
            <div class="date-block me-3">
              <span class="month">{{ trade.publicationDate | date: "%b" | upcase }}</span>
              <span class="day">{{ trade.publicationDate | date: "%d" }}</span>
            </div>
            <div class="flex-grow-1">
              <h5 class="card-title h6">{{ trade.tradeTitle }}</h5>
              <p class="card-text small text-muted"><strong>Return:</strong> {{ trade.expectedReturnDisplay }}</p>
              <p class="card-text small mt-2">{{ trade.summaryJustification }}</p>
            </div>
          </div>
          <div class="card-footer bg-white border-top-0 pt-0">
            <div class="d-flex flex-wrap" style="gap: 0.5rem; margin-left: 81px;">
              <a href="https://www.google.com/search?q={{ trade.ticker }}+stock" target="_blank" rel="noopener noreferrer" class="btn btn-sm btn-outline-primary"><i class="fas fa-chart-line fa-fw me-1"></i> View Chart</a>
              <button onclick="copyTradeDetails(this)" class="btn btn-sm btn-outline-secondary" title="Copy trade details"><i class="fas fa-copy fa-fw me-1"></i> Copy Details</button>
              <div class="trade-details-data" style="display: none;">
                {{ trade.tradeTitle }}
                - Strategy: {{ trade.analysis.strategyType }}
                - Expiration: {{ trade.analysis.tradeDetails.expiration | date: "%Y-%m-%d" }}
                - Strike: {{ trade.analysis.tradeDetails.putStrike }}
                - Premium: ${{ trade.analysis.tradeDetails.putPremium }}
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
  // Copy function for trade details
  function copyTradeDetails(button) {
    const detailsContainer = button.nextElementSibling;
    const detailsText = detailsContainer.textContent.trim().replace(/\s+/g, ' '); // Clean up whitespace

    navigator.clipboard.writeText(detailsText).then(() => {
      const originalIcon = button.innerHTML;
      button.innerHTML = '<i class="fas fa-check fa-fw me-1"></i> Copied!';
      const originalClasses = Array.from(button.classList);

      button.classList.remove('btn-outline-secondary');
      button.classList.add('btn-success');

      setTimeout(() => {
        button.innerHTML = originalIcon;
        button.classList.remove('btn-success');
        originalClasses.forEach(c => button.classList.add(c));
      }, 2000);
    }).catch(err => {
      console.error('Failed to copy text: ', err);
    });
  }
</script>
