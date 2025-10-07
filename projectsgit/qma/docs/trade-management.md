---
layout: projectgit
title: "Trade Management Guide"
project: qma
repo: mkahveci/qma
permalink: /:path/:basename:output_ext
---

<style>
  .guide-section {
    padding: 1.5rem;
    margin-bottom: 2rem;
    border-radius: 0.5rem;
    background-color: #f8f9fa;
  }
  .guide-title {
    color: #495057;
    font-weight: bold;
    font-size: 1.5rem;
    margin-bottom: 1rem;
  }
  .strategy-header {
    font-size: 1.25rem;
    font-weight: bold;
    color: #007bff;
    border-bottom: 2px solid #007bff;
    padding-bottom: 0.5rem;
    margin-top: 2rem;
  }
  .list-strategy li {
    margin-bottom: 0.5rem;
    line-height: 1.5;
  }
  .list-strategy strong {
    color: #212529;
  }
  .callout {
    background-color: #e2f2ff;
    border-left: 5px solid #007bff;
    padding: 1rem;
    margin-top: 1rem;
    border-radius: 0.25rem;
  }
</style>

<div class="container my-5">
  <div class="text-center mb-5">
    <h1 class="display-5 fw-bold">TastyTrade Trade Management Strategies</h1>
    <p class="lead col-lg-8 mx-auto">
      Successful options trading isn't just about finding the right entry; it's about disciplined trade management. This guide outlines the core mechanics for managing premium-selling positions, inspired by the principles of TastyTrade.
    </p>
  </div>

  <div class="guide-section shadow-sm">
    <h2 class="guide-title">The "45 DTE" Strategy: Short Put</h2>
    <p>This is a foundational strategy for selling premium. By entering a short put position with roughly 45 days to expiration, we capture a significant amount of theta (time decay) while giving the underlying stock ample time to stay above our short strike. The key is to manage the trade based on time and profit targets, not just price movement.</p>

    <div class="strategy-header">Entry Criteria</div>
    <ul class="list-unstyled list-strategy">
      <li><strong>Target DTE:</strong> Approximately 45 days. This provides the ideal balance of capturing premium while mitigating the risk of rapid, unpredictable price moves.</li>
      <li><strong>Strike Selection:</strong> Choose a strike with a <b>.15 to .30 delta</b>. This gives us a high probability of profit (around 70-85% at entry) and puts the strike well outside of the expected one-standard-deviation move.</li>
      <li><strong>IV Rank:</strong> Only enter trades when the <b>Implied Volatility (IV) Rank is 30% or higher</b>. High IV means options are relatively expensive, allowing us to collect more premium for the same risk.</li>
    </ul>

    <div class="strategy-header">Management Plan</div>
    <ul class="list-unstyled list-strategy">
      <li><strong>Profit Taking:</strong> The primary goal is to <b>take profits at 50% of the maximum potential profit</b>. Once the option's value has decayed by half, we close the position. This allows us to redeploy capital and reduce risk, as the final 50% of the premium takes significantly longer to decay than the first.</li>
      <li><strong>Time-Based Management:</strong> If the trade has not hit the 50% profit target but reaches <b>21 Days to Expiration (DTE)</b>, we consider closing the trade. This is because the rate of theta decay accelerates in the final three weeks, making it more volatile and less predictable. By closing early, we avoid this "gamma risk."</li>
      <li><strong>Adjusting/Closing for Loss:</strong> If the underlying stock price moves against the position and the short put becomes at-the-money, it's often best to close the position and move on. The loss is controlled, and you can seek a new, high-probability trade elsewhere.</li>
    </ul>
    <div class="callout">
      <strong>Analogy:</strong> Think of it like a professional gambler. You bet on the odds being in your favor, and once you've collected a significant portion of your expected win, you leave the table. You don't stay to capture the last few dollars and risk losing everything on a bad hand.
    </div>
  </div>

  <div class="guide-section shadow-sm">
    <h2 class="guide-title">The "Wheel" Strategy: Weekly Short Put</h2>
    <p>The "Wheel" is an income-generating strategy that involves three steps: selling puts, getting assigned shares, and then selling covered calls. This guide focuses on the first step: selling a weekly put to collect premium. This strategy works best on stocks you're willing to own at a discount.</p>

    <div class="strategy-header">Entry Criteria</div>
    <ul class="list-unstyled list-strategy">
      <li><strong>Target DTE:</strong> Approximately <b>7 days</b> (a weekly expiration). The goal is rapid theta decay and quick capital turnover.</li>
      <li><strong>Strike Selection:</strong> Choose a strike with a <b>.15 to .30 delta</b>. This maximizes the probability of success while still collecting meaningful premium.</li>
      <li><strong>Annualized ROC:</strong> The annualized Return on Capital (ROC) <b>must be greater than 30%</b>. This ensures the premium collected justifies the weekly risk, making the trade financially worthwhile. The formula is: <code>(Premium / Strike Price) * (365 / DTE)</code>.</li>
    </ul>

    <div class="strategy-header">Management Plan</div>
    <ul class="list-unstyled list-strategy">
      <li><strong>Profit Taking:</strong> The ultimate goal is to <b>close the position as soon as it reaches 80% of max profit</b>, even if this happens in the first day. This is a key difference from the 45 DTE strategy. The high annualized ROC means we want to close winners quickly to redeploy capital.</li>
      <li><strong>Holding to Expiration:</strong> If the trade is still a winner at expiration, it will simply expire worthless. This is the ideal outcome.</li>
      <li><strong>Assignment (The "Wheel"):</strong> If the stock price falls below the short put strike at expiration, the put will be assigned, and you will buy 100 shares of the stock at the strike price. This is not a failure—it's the second step of the Wheel.</li>
    </ul>
    <div class="callout">
      <strong>Next Step: Selling Covered Calls.</strong> Once assigned shares, the next step is to sell covered calls on those shares. You'll continue to collect premium until the shares are called away (sold) at a higher price, completing the "Wheel."
    </div>
  </div>
</div>