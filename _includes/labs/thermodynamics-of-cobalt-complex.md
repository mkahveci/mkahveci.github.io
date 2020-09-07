## 1 Goals

### 1.1 Calculate the equilibrium concentration

- Calculate the equilibrium concentration of tetrachlorocobaltate(II) in solution at each temperature using Beer’s law with the measured absorbance value at the temperature of interest.

{% include eq.html file="evj-1.svg" %}

- Assume that the molar absorptivity, _b_, of CoCl<sub>2</sub><sup>2+</sup> in water at 690 nm is constant (6.00 × 10<sup>2</sup> M<sup>-1</sup>.cm<sup>-1</sup> for all 4 temperature values.
- The path length, _a_, is equal to 1.00 cm.

- The equilibrium concentration of uncomplexed cobalt(II), Co<sup>2+</sup>,  ions in solution at any given temperature is found using conservation of mass, the initial concentration of cobalt(II) ions in the stock solution, and the equilibrium concentration of tetrachlorocobaltate(II) at that temperature.

### 1.2 Calculate the equilibrium constant

- Calculate the equilibrium constant for the reaction of interest at each temperature using Equation 2.

{% include eq.html file="evj-2.svg" %}

In doing this calculation, assume that the [Cl<sup>-</sup>] is constant due to the presence of strong 6.00 M HCl acid. For the sake of significant figures in this calculation, assume the concentration of HCl is exactly 6.00 M.

### 1.3 Calculate the equilibrium concentration of uncomplexed cobalt(II)

{% include eq.html file="evj-3.svg" %}

The equilibrium concentration of uncomplexed cobalt(II), Co<sup>2+</sup>, ions in solution at any given temperature is found using conservation of mass (i.e. the stoichiometric calculation based on Eqation 3), the initial concentration of cobalt(II) ions in the stock solution, and the equilibrium concentration of tetrachlorocobaltate(II) at that temperature.

### 1.4 Calculate _ΔG<sup>◦</sup>_ using _K_

- Calculate _ΔG<sup>◦</sup>_ at each temperature studied for each trial using Equation 4.

{% include eq.html file="evj-4.svg" %}

where R = 8.3145 J/mol.K (use all figures to ensure proper significant figures), and all temperature values are in Kelvin.

### 1.5 Make ln _K_ vs. 1/_T_ plots

- Make ln _K_ vs. 1/_T_ plots for each trial separately.
- Temperature values are in Kelvin.
- Using the Excel formulas, calculate slope, `=SLOPE()`, and intercept `=INTERCEPT()` for the line of best fit.
- Calculate _ΔH<sup>◦</sup>_ and _ΔS<sup>◦</sup>_ for each trial using Equation 5.

{% include eq.html file="evj-5.svg" %}

where slope =  - ( _ΔH<sup>◦</sup>_ / R ), _y-_ intercept =  ( _ΔS<sup>◦</sup>_ / R ), _R_ is in energy unit like in Equation 4, and temperature is in Kelvin.

### 1.6 Calculate _ΔG<sup>◦</sup>_ using _ΔH<sup>◦</sup>_ and _ΔS<sup>◦</sup>_

- Calculate _ΔG<sup>◦</sup>_ at each temperature studied for each trial using Equation 6.

{% include eq.html file="evj-6.svg" %}

where _T_ is in Kelvin. 

- Assume that _ΔH<sup>◦</sup>_ and _ΔS<sup>◦</sup>_ are constant with temperature.

### 1.7 Generate a combined plot of ln _K_ vs. 1/_T_

- Generate a combined plot of ln _K_ vs. 1/_T_. In this plot, you should include the results from all trials.

## 2 Assignment

- Watch the videos, pass the postlab quiz, and download your data set
- Analyze the data in Excel
- Submit your __full lab report__ in a PDF file and __calculations__ in an Excel file.
  - Be sure to fully discuss your results.
    - Compare the values from the two trials and discuss how similar or different they are, as well as potential reasons for differences observed.
    - Discuss the values of $$ \Delta G^\circ $$: are the values obtained similar for each type of calculation? Why might they be different?
  - There are two discussion prompts that should be incorporated into your overall discussion
    - One relates to the signs of $$ \Delta H^\circ $$ and $$ \Delta S^\circ $$, and why the signs you obtained do or do not follow your expectations.
    - The other relates to the conditions for spontaneity. Remember that $$ \Delta H^\circ $$ and $$ \Delta S^\circ $$  relate to standard state conditions when you calculate the temperature range over which the reaction will occur spontaneously. 
- You should review the `Lab Report Guidelines`, `Sample General Chemistry Lab Report`, and `Appendix E` on D2L while writing to ensure that your drafts are correctly formatted.

## 3 Q&A Highlights

### 3.1 Calculating the equilibrium concentration of Co<sup>2+</sup>

{% include callout.html content=" I had a question on how to calculate the equilibrium concentration of Co<sup>2+</sup>. In the lab, it gives a brief description but no equation." type="danger" %}

To answer this question, a new subsection was added to this document. Please [see]({{ site.urlx }}/evj#13-calculate-the-equilibrium-concentration-of-uncomplexed-cobaltii): Calculate the equilibrium concentration of uncomplexed cobalt(II)

## 4 Assessment 

### 4.1 Feedback

- The PDF file you uploaded: annotations are highlighted with gray background and pink font.
- E-Rubric: D2L will show the rubric with scores and any feedback provided.

### 4.2 Grades 

<table>
<caption>Table 1. Grade stats for this experiment.</caption>
<thead>
  <tr>
    <th>Term Statistics<sup>a</sup></th>
    <th>Average</th>
    <th>Stdev</th>
    <th>Median</th>
    <th>Maximum</th>
    <th>Minimum</th>
  </tr>
</thead>
<tfoot>
    <tr>
        <td colspan="6"><sup>a</sup>All zero values are excluded.</td>
    </tr>
</tfoot>
<tbody>
  <tr>
    <td>SSQ 2020</td>
    <td>79.30%</td>
    <td>13.65%</td>
    <td>76.17%</td>
    <td>97.00%</td>
    <td>52.83%</td>
  </tr>
</tbody>
</table>

### 4.3 Team grading 

<table>
<caption>Table 2. Task sharing for team grading based on the sections of the rubric.</caption>
<thead>
  <tr>
    <th>Instructor</th>
    <th>Teaching Assistant</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>Overall Clarity and Flow</td>
    <td>Procedure</td>
  </tr>
  <tr>
    <td>Abstract</td>
    <td>Table Formatting</td>
  </tr>
  <tr>
    <td>Proofreading and General Formatting</td>
    <td>Figure Formatting</td>
  </tr>
  <tr>
    <td>Results</td>
    <td>Prelab</td>
  </tr>
  <tr>
    <td>Discussion</td>
    <td>Postlab</td>
  </tr>
  <tr>
    <td>ln K vs. 1/T Figures</td>
    <td>Temperature Study Table</td>
  </tr>
  <tr>
    <td>Discussion Prompts</td>
    <td>Free Energy Comparison Table</td>
  </tr>   
  <tr>
    <td></td>
    <td>Excel Calculations</td>
  </tr>         
</tbody>
</table>