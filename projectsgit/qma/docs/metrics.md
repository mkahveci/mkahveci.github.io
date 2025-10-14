---
layout: projectgit
title: "Understanding the Calculations"
project: qma
repo: mkahveci/qma
permalink: /:path/:basename:output_ext
---

## Understanding the Calculations: A Guide to TastyTrade Metrics

### Max Profit

* **Description:** The total potential profit you can achieve on the trade, which is equal to the premium collected from selling the option.
* **Formula:** The premium is per share, so it must be multiplied by 100 shares per contract.

$$\text{Max Profit} = \text{Put Premium} \times 100$$

---

### ROC (Return on Capital)

* **Description:** The return on the capital risked for a single trade. It's a quick measure of the trade's efficiency.
* **Formula:** This is calculated by dividing the max profit by the full notional value (the total value of the shares you are at risk of being assigned).

$$\text{ROC} = \frac{\text{Max Profit}}{\text{Put Strike} \times 100}$$

---

### Annualized ROC (Linear)

* **Description:** This metric projects the trade's ROC over a full year, assuming you can repeat a similar trade with the same capital. This is a crucial metric for comparing the efficiency of trades with different durations (DTEs).
* **Formula:** The ROC is scaled up to a 365-day period based on the trade's duration.

$$\text{Annualized ROC} = \text{ROC} \times \frac{365}{\text{DTE}}$$

---

### Annualized Return (Compounded)

* **Description:** This is a more precise, academic calculation that assumes you can reinvest your earnings from each trade. This method is considered more accurate for showing the potential long-term growth of a strategy, as it accounts for the power of compounding.
* **Formula:** This uses the principle of compounding interest to project the return over a year.

$$\text{Annualized Return} = \left(1 + \text{ROC}\right)^{\frac{365}{\text{DTE}}} - 1$$

---

### Buying Power

* **Description:** The amount of capital required to open and hold the trade. For a short put, this is the full notional value of the contract.
* **Formula:**

$$\text{Buying Power} = \text{Put Strike} \times 100$$

---

### Daily Profit Potential

* **Description:** The average amount of profit you can expect to earn per day the trade is open. This is especially useful for comparing weekly trades.
* **Formula:**

$$\text{Daily Profit Potential} = \frac{\text{Max Profit}}{\text{DTE}}$$

---

### POP (Probability of Profit)

* **Description:** The estimated probability that the trade will be profitable at expiration.
* **Formula:** This is generally approximated using the option's delta. For a short put, the probability of profit is approximately:

$$\text{POP} \approx 1 - \text{Delta}$$