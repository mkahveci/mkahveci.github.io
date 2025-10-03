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

              {%- assign strike_string = trade.analysis.tradeDetails.putStrike | append: '' -%}
              {%- assign strike_parts = strike_string | split: '.' -%}
              {%- if strike_parts[1].size == 1 -%}
                {%- assign formatted_strike = strike_string | append: '0' -%}
              {%- else -%}
                {%- assign formatted_strike = strike_string -%}
              {%- endif -%}

              {%- assign premium_string = trade.analysis.tradeDetails.putPremium | append: '' -%}
              {%- assign premium_parts = premium_string | split: '.' -%}
              {%- if premium_parts[1].size == 1 -%}
                {%- assign formatted_premium = premium_string | append: '0' -%}
              {%- else -%}
                {%- assign formatted_premium = premium_string -%}
              {%- endif -%}
              <h5 class="card-title h6">{{ trade.tradeTitle }}</h5>
              <p class="card-text small text-muted"><strong>Return:</strong> {{ trade.expectedReturnDisplay }}</p>
              <p class="card-text small mt-2">{{ trade.summaryJustification }}</p>

              <ul class="list-unstyled small mt-3 mb-0">
                <li class="d-flex justify-content-between border-top pt-2">
                  <span><strong>Strategy:</strong></span>
                  <span class="font-monospace">{{ trade.analysis.strategyType }}</span>
                </li>
                <li class="d-flex justify-content-between pt-1">
                  <span><strong>Expiration:</strong></span>
                  <span class="font-monospace">{{ trade.analysis.tradeDetails.expiration | date: "%Y-%m-%d" }}</span>
                </li>
                <li class="d-flex justify-content-between pt-1">
                  <span><strong>Strike:</strong></span>
                  <span class="font-monospace">{{ formatted_strike }}</span>
                </li>
                <li class="d-flex justify-content-between pt-1">
                  <span><strong>Premium:</strong></span>
                  <span class="font-monospace">${{ formatted_premium }}</span>
                </li>
              </ul>
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
                - Strike: {{ formatted_strike }}
                - Premium: ${{ formatted_premium }}
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