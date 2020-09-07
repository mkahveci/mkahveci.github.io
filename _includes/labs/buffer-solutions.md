## 1 Goals

### 1.1 Prepare the buffers A1-E1

- Calculate the concentration of each component present in buffers A1-E1 using the concentration of each stock solution, the volume of each solution delivered, and the total volume of buffer created.

<table>
<caption>Table 1. Preparing buffer solutions.</caption>
<thead>
  <tr>
    <th>Solution</th>
    <th>Volume (mL) of CH<sub>3</sub>COOH or NH<sub>4</sub>Cl</th>
    <th>Volume (mL) of CH<sub>3</sub>COONa or NH<sub>3</sub></th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>A1</td>
    <td>15.00</td>
    <td>15.00</td>
  </tr>
  <tr>
    <td>B1</td>
    <td>20.00</td>
    <td>10.00</td>
  </tr>
  <tr>
    <td>C1</td>
    <td>25.00</td>
    <td>5.00</td>
  </tr>
  <tr>
    <td>D1</td>
    <td>5.00</td>
    <td>25.00</td>
  </tr>
  <tr>
    <td>E1 </td>
    <td>10.00</td>
    <td>20.00</td>
  </tr>           
</tbody>
</table>

### 1.2 Generate the plot of pH vs. log([base]/[acid])

- Fit the data to a line (i.e. trendline). 
- Calculate the slope (3 sig. figs required) using `=SLOPE()` function in Excel.
- Calculate the intercept (3 sig. figs required) using `=INTERCEPT()` function in Excel.

### 1.3 Generate the plot pH vs. the logarithm of the dilution factor

- Generate a single scatter plot of pH vs. the logarithm of the dilution factor (1, 10, 100) for each buffer component using Excel.
- Both data sets should be presented on the same plot.
- Do not fit the data to a trendline.

## 2 Assignment

- Watch pH meter calibration video
- Watch the videos, pass the postlab quiz, and download your data set for Experiment 6
- Analyze the data in Excel
- Submit your partial lab report in a PDF file and all calculations in an Excel file.
- You should review the `Lab Report Guidelines`, `Sample General Chemistry Lab Report`, and `Appendix E` on D2L while writing to ensure that your drafts are correctly formatted.

## 3 Q&A Highlights

### 3.1 Total volumes of buffer solutions

{% include callout.html content="I'm not confident which volumes I should use as my volume delivered and total volume. Should I add the volumes of NH<sub>4</sub>Cl and NH<sub>3</sub> together as my volume delivered? In my Excel calculations, I then added 75mL from HCl for my total volume for A1, C1, and D1. The procedure mentions adding HCl to A1, C1, and D1, but I'm not sure what I need to incorporate into my total volume for B1 and E1 since the procedure doesn't say much else about them, or what to do with A2." type="danger" %}

First of all, please try to make your questions more concise. It is a little hard to follow what is being asked here. Perhaps, sending your existing work might help clarify your confusion easier.

According to Table 2, solution A1 has the following total volume:

{% include eq.html file="fbo-1.svg" %}

{% include eq.html file="fbo-2.svg" %}

Likewise, sum the volume values of each species for B1, C1, D1, and E1 to calculate their respective V<sub>tot</sub> values.  

Next step is about addition of HCl solution. `Obtain 75 mL of 0.10 M hydrochloric acid and 75 mL of 0.10 M sodium hydroxide. Add 10 mL of hydrochloric acid to solutions A1, C1, D1, and Water 1.`

I will show the volume calculation for A1 only. 10.00 mL HCl solution is added to A1. Thus:

{% include eq.html file="fbo-3.svg" %}

{% include eq.html file="fbo-4.svg" %}

## 4 Assessment

### 4.1 Misconceptions

#### 4.1.1 Henderson-Hasselbalch plot

- The plot should have one data series
- Variables are confused:
  - _x-_ axis should be {% include eq.html file="fbo-5.svg" inline=true %}. 
    - One refers to this variable as `Henderson-Hasselbalch constant`. 
      - How can a constant be a variable at the same time, plotted in the $$x-$$axis?
      - So, common sense can easily avoid some confusions[^1].
  - See the relevant instructions [above]({{ site.urlx }}/fbo#12-generate-the-plot-of-ph-vs-logbaseacid).  

[^1]: Being confused is good because it means you are learning. _Can you learn without thinking? Can you think without any confusion? Can you get confused without any desire to learn?..._  

{% include callout.html content="Log[base/acid]" type="danger" %}

It should be {% include eq.html file="fbo-5.svg" inline=true %}. Bracket represents molarity. Bracket of base/acid does not represent molarity.

#### 4.1.2 Dilution plot

- Variables are confused:
  - _x-_ axis should be log(dilution factor).
  - See the relevant instructions [above]({{ site.urlx }}/fbo#13-generate-the-plot-ph-vs-the-logarithm-of-the-dilution-factor).

### 4.3 Formatting Issues

{% include callout.html content="NH3 and NH4" type="danger" %}

Should be writte as: NH<sub>3</sub> and NH<sub>4</sub><sup>+</sup>

#### 4.3.1 Data table

- Sig. fig. errors. For example:
  - Presented: 
    - 0 mL
    - 5 mL
  - Expected:
    - 0.00 mL
    - 5.00 mL  
- Title is missing

### 4.4 Feedback

- The PDF file you uploaded: annotations are highlighted with gray background and pink font.
- E-Rubric: D2L will show the rubric with scores and any feedback provided.

### 4.5 Grades 

<table>
<caption>Table 2. Grade stats for this experiment.</caption>
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
    <td>88.55%</td>
    <td>8.19%</td>
    <td>91.80%</td>
    <td>100.00%</td>
    <td>73.00%</td>
  </tr>
</tbody>
</table>

### 4.6 Team grading

<table>
<caption>Table 3. Task sharing for team grading based on the sections of the rubric.</caption>
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
    <td>Results</td>
    <td>Figure Formatting</td>
  </tr>
  <tr>
    <td>Proofreading and General Formatting</td>
    <td>Prelab</td>
  </tr>
  <tr>
    <td>Strong Acid-Strong Base Data Table</td>
    <td>Postlab</td>
  </tr>
  <tr>
    <td>Henderson-Hasselbalch Plot</td>
    <td>Excel Calculations</td>
  </tr>
  <tr>
    <td>Dilution Plot</td>
    <td></td>
  </tr>
  <tr>
    <td>Discussion</td>
    <td></td>
  </tr>             
</tbody>
</table>