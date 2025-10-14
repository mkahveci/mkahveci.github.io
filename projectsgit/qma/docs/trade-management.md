---
layout: projectgit
title: "Trade Management Guide"
project: qma
repo: mkahveci/qma
permalink: /:path/:basename:output_ext
---

# TastyTrade Trade Management Strategies

*Successful options trading isn't just about finding the right entry; it's about disciplined trade management. This guide outlines the core mechanics for managing premium-selling positions, inspired by the principles of TastyTrade.*

## The "45 DTE" Strategy: Short Put

This is a foundational strategy for selling premium. By entering a short put position with roughly 45 days to expiration, we capture a significant amount of theta (time decay) while giving the underlying stock ample time to stay above our short strike. The key is to manage the trade based on time and profit targets, not just price movement.

### Entry Criteria

* **Target DTE:** Approximately 45 days. This provides the ideal balance of capturing premium while mitigating the risk of rapid, unpredictable price moves.

* **Strike Selection:** Choose a strike with a **.15** to **.30 delta**. This gives us a high probability of profit (around 70-85% at entry) and puts the strike well outside of the expected one-standard-deviation move.

* **IV Rank:** Only enter trades when the **Implied Volatility (IV) Rank is 30% or higher**. High IV means options are relatively expensive, allowing us to collect more premium for the same risk.

### Management Plan

* **Profit Taking:** The primary goal is to **take profits at 50% of the maximum potential profit**. Once the option's value has decayed by half, we close the position. This allows us to redeploy capital and reduce risk, as the final 50% of the premium takes significantly longer to decay than the first.

* **Time-Based Management:** If the trade has not hit the 50% profit target but reaches **21 Days to Expiration (DTE)**, we consider closing the trade. This is because the rate of theta decay accelerates in the final three weeks, making it more volatile and less predictable. By closing early, we avoid this "gamma risk."

* **Adjusting/Closing for Loss:** If the underlying stock price moves against the position and the short put becomes at-the-money, it's often best to close the position and move on. The loss is controlled, and you can seek a new, high-probability trade elsewhere.

> **Analogy:** Think of it like a professional gambler. You bet on the odds being in your favor, and once you've collected a significant portion of your expected win, you leave the table. You don't stay to capture the last few dollars and risk losing everything on a bad hand.

## The "Wheel" Strategy: Weekly Short Put

The "Wheel" is an income-generating strategy that involves three steps: selling puts, getting assigned shares, and then selling covered calls. This guide focuses on the first step: selling a weekly put to collect premium. This strategy works best on stocks you're willing to own at a discount.

### Entry Criteria

* **Target DTE:** Approximately **7 days** (a weekly expiration). The goal is rapid theta decay and quick capital turnover.

* **Strike Selection:** Choose a strike with a **.15 to .30 delta**. This maximizes the probability of success while still collecting meaningful premium.

* **Annualized ROC:** The annualized Return on Capital (ROC) **must be greater than 30%**. This ensures the premium collected justifies the weekly risk, making the trade financially worthwhile. The formula is: $$ \left(\frac{\text{Premium}}{\text{Strike Price}}\right) \left(\frac{365}{\text{DTE}}\right) $$.

### Management Plan

* **Profit Taking:** The ultimate goal is to **close the position as soon as it reaches 80% of max profit**, even if this happens in the first day. This is a key difference from the 45 DTE strategy. The high annualized ROC means we want to close winners quickly to redeploy capital.

* **Holding to Expiration:** If the trade is still a winner at expiration, it will simply expire worthless. This is the ideal outcome.

* **Assignment (The "Wheel"):** If the stock price falls below the short put strike at expiration, the put will be assigned, and you will buy 100 shares of the stock at the strike price. This is not a failure—it's the second step of the Wheel.

> **Next Step: Selling Covered Calls.** Once assigned shares, the next step is to sell covered calls on those shares. You