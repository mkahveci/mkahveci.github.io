---
layout: default 
title: Trade Performance Analysis 
permalink: /performance/
published: true
sitemap: false
---

<!-- CRITICAL FIX 1: Corrected Chart.js URL to direct CDN link -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.3/dist/chart.umd.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-date-fns@3"></script>


<h1>Trading Performance Dashboard</h1>
<p class="lead">
  Analysis generated on 
  <strong>{{ site.data.performance_report.metadata.generated_at | date: "%B %d, %Y at %I:%M %p" }}</strong>,
  showing realized P&L from 
  {{ site.data.performance_report.metadata.start_date }} 
  to 
  {{ site.data.performance_report.metadata.end_date }}.
</p>

<!-- STATS CARDS -->
<div style="display: flex; gap: 20px; margin-bottom: 30px; flex-wrap: wrap;">
  <div class="stat-card">
    <h3>Total Net P&L</h3>
    {% assign pnl = site.data.performance_report.total_summary.total_net_pnl %}
    <p class="data-main-value {% if pnl >= 0 %}positive{% else %}negative{% endif %}">${{ pnl | round: 2 }}</p>
  </div>

  <div class="stat-card">
    <h3>Total Trades Closed</h3>
    <p class="data-main-value">{{ site.data.performance_report.total_summary.total_trades_closed }}</p>
  </div>

  <div class="stat-card">
    <h3>Total Commissions</h3>
    <p class="data-main-value">${{ site.data.performance_report.total_summary.total_commissions | round: 2 }}</p>
  </div>

  <div class="stat-card">
    <h3>Total Fees</h3>
    <p class="data-main-value">${{ site.data.performance_report.total_summary.total_fees | round: 2 }}</p>
  </div>
</div>
<!-- End STATS CARDS -->

<!-- CUMULATIVE P&L CHART -->
<h2>Cumulative Performance Over Time</h2>
{% if site.data.performance_report.time_series_data.daily_net_pnl %}
{% include trade_chart.html %}
{% else %}
  <p>Time series data is missing for charting. Please ensure the Python script executed completely and saved the JSON file.</p>
{% endif %}

<!-- INDIVIDUAL TRADES TABLE -->
<h2>Individual Trade History (Closed)</h2>

{% if site.data.performance_report.individual_trades %}
<table class="trade-table">
  <thead>
    <tr>
      <th>Date & Time</th>
      <th>Symbol</th>
      <th>Gross P&L</th>
      <th>Fees</th>
      <th>Commissions</th>
      <th>Net P&L</th>
    </tr>
  </thead>
  <tbody>
    {% assign trades = site.data.performance_report.individual_trades | sort: 'executed_at' | reverse %}
    {% for trade in trades %}
      {% assign net_pnl = trade.net_pnl | minus: trade.fees | minus: trade.commissions %}
      <tr class="{% if trade.net_pnl >= 0 %}trade-win{% else %}trade-loss{% endif %}">
        <td>{{ trade.executed_at | date: "%Y-%m-%d %H:%M:%S" }}</td>
        <td><strong>{{ trade.symbol }}</strong></td>
        <td>${{ trade.net_pnl | round: 2 }}</td>
        <td>${{ trade.fees | round: 2 }}</td>
        <td>${{ trade.commissions | round: 2 }}</td>
        <td>${{ net_pnl | round: 2 }}</td>
      </tr>
    {% endfor %}
  </tbody>
</table>
{% else %}
  <p>Trade history data is not yet available or contains no closed trades. Please ensure the Python script has run successfully.</p>
{% endif %}

<style>
/* Basic, modern CSS for the Jekyll output */
:root {
  --color-primary: #007bff;
  --color-success: #28a745;
  --color-danger: #dc3545;
  --color-neutral: #f8f9fa;
  --shadow-light: 0 4px 6px rgba(0, 0, 0, 0.1);
}

body {
  font-family: 'Arial', sans-serif;
  padding: 20px;
}

.lead {
  font-style: italic;
  color: #6c757d;
  margin-bottom: 30px;
  border-bottom: 1px solid #e9ecef;
  padding-bottom: 15px;
}

.stat-card {
  background: var(--color-neutral);
  padding: 20px;
  border-radius: 8px;
  box-shadow: var(--shadow-light);
  flex: 1;
  min-width: 200px;
  text-align: center;
}

.stat-card h3 {
  font-size: 1.1em;
  color: #495057;
  margin-top: 0;
  margin-bottom: 10px;
}

.data-main-value {
  font-size: 2em;
  font-weight: bold;
  color: #343a40;
}

.positive { color: var(--color-success); }
.negative { color: var(--color-danger); }

/* Table Styles */
.trade-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  box-shadow: var(--shadow-light);
  border-radius: 8px;
  overflow: hidden; /* Ensures rounded corners clip content */
}

.trade-table thead {
  background-color: var(--color-primary);
  color: white;
}

.trade-table th,
.trade-table td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #dee2e6;
}

.trade-table tbody tr:hover {
  background-color: #e9f5ff;
}

.trade-win { background-color: #e6ffed; }  /* Light green for wins */
.trade-loss { background-color: #ffebeb; } /* Light red for losses */
</style>
