## 1 Goals

### 1.1 Generate the standard curve

- Mass by difference calculate the mass of the known steel sample.
- The percent by mass of the known steel sample is known as 0.94% Mn.
  - Using the mass of the known steel sample and the weight to weight percent of Mn in this sample, calculate the mass and moles of Mn in the sample. Use Equation 1 and 2.

{% include eq.html file="ksm-1.svg" %}

{% include eq.html file="ksm-2.svg" %}

  - Calculate the molarity of known steel sample solution using Equations 3 and 4.

{% include eq.html file="ksm-3.svg" %}

{% include eq.html file="ksm-4.svg" %}

- Using Equation 5, calculate the concentrations of each diluted solutions of MnO<sub>4</sub><sup>-</sup>$$. Remember that the dilutions were 3:1, 2:2, and 1:3 volume to volume ratio. 

{% include eq.html file="ksm-5.svg" %}

- Generate a standard curve (absorbance at  525 nm vs. concentration of MnO<sub>4</sub><sup>-</sup> in M) for the solutions of known MnO<sub>4</sub><sup>-</sup> concentration.
  - In doing so, add 0 absorbance, 0 molar values as well. 
  - Thus, in total there are five data points in this plot.

### 1.2 Determine the molar absorptivity

- Apply trendline analysis over the standard curve.
- Following Beer’s Law, Equation 6, the slope of the plot determines the molar absorptivity _a_ of MnO<sub>4</sub><sup>-</sup>.

{% include eq.html file="ksm-6.svg" %}

where the path length, b = 1.00 cm.

{% include eq.html file="ksm-7.svg" %}

### 1.3 Calculate the concentration of unknown steel solution

- Use Equation 6 to calculate the concentration, _c_ of MnO<sub>4</sub><sup>-</sup>.
- Probably your data has three trials of absorbance value.
- Repeat this calculation over all trials.
- Calculate the average concentration of MnO<sub>4</sub><sup>-</sup>, and also report the standard deviation.

### 1.4 Calculate %Mn in the unknown steel sample

- This is a straightforward calculation as you will be plugging in the average concentration of MnO<sub>4</sub><sup>-</sup> in Equation 8.

{% include eq.html file="ksm-8.svg" %}

where m_<sub>sample</sub> is the mass of unknown sample; V<sub>MnO<sub>4</sub><sup>-</sup></sub> is the total volume of unknown sample solution, which is 250.00 mL; MnO<sub>4</sub><sup>-</sup> is the average concentration of MnO<sub>4</sub><sup>-</sup> in the unknown solution (calculated in subsection [1.3](/ksm#13-calculate-the-concentration-of-unknown-steel-solution)).

## 2 Assignment

- Compare the molar absorptivity from your plot to the literature value
given in the lab instructions.
- Read the lab instructions carefully so you can explain why you do or do not have to worry about Cu<sup>2+</sup> and Ni<sup>2+</sup> ions interfering with your results.
- Think through how a molar absorptivity that is too low would affect your results. To answer this correctly, follow the computational steps to make sure you can clearly state if an a value that is too small will lead to a higher or lower percent Mn than the correct value.
- Incorporate the responses to the above prompts in your overall discussion. Be sure to discuss the quality of your fit, the spread in the absorbance readings for the unknown, etc. to ensure your discussion is complete.
- Watch the videos, pass the postlab quiz, and download your data set.
- Submit your __full lab report__ in a PDF file and __calculations__ in an Excel file.
- You should review the `Lab Report Guidelines`, `Sample General Chemistry Lab Report`, and `Appendix E` on D2L while writing to ensure that your drafts are correctly formatted.

## 3 Q&A Highlights

### 3.1 Taking the prelab quiz

{% include callout.html content="Is there anyway you can give me an example of how to enter the answers for the calculations? I just can’t seem to figure that out." type="danger" %}

Please pay attention to the values of calculations. The values should be entered with correct significant figures and units. Units are case sensitive. Use the SI unit conventions.

For example:

- `1250` is not equal to `1250.`
- `L` is not equal to `l`

### 3.2 Calculations

{% include callout.html content="I would like to attend your office hours at 4pm tomorrow to ask a couple questions about the calculations for Experiment 10." type="danger" %}

After this meeting, the Goals section was revised. Although the lecture notes were elaborate enough, now this page has more details with relevant formulae, for those of whom are confused[^1]. 

[^1]: Being confused is good because it means you are learning. _Can you learn without thinking? Can you think without any confusion? Can you get confused without any desire to learn?..._

### 3.3 The unit of absorbance

{% include callout.html content="I was wondering if there are units that are necessary for the absorbance values on the figure needed for this lab." type="danger" %}

Absorbance does not have a unit. The absorbance, _A_, is defined by the incident intensity, _I<sub>0</sub>_, and transmitted intensity, _I_.

{% include eq.html file="ksm-9.svg" %}

Overall, the equation shows no unit.

### 3.4 The concentration of undiluted solution

{% include callout.html content="I am confused on where the fifth point on the standard curve graph comes from. I know that there is supposed to be a point where it is at the origin so I added that in the curve but since the volume of the diluted water is 0 isn’t the concentration of MnO<sub>4</sub><sup>-</sup> also 0? If it is then it is way off the trend line and I don’t know what I did wrong. Please let me know if you can help me figure out what I did wrong that made the point for 1.610 absorbance have 0 concentration." type="danger" %}

I suspect a `potential misunderstanding` here. When there is an aqueous solution, it is mostly water. Water is the `solvent`, so by definition solvent is in abundance. When the solution is diluted, more water added. This is an important point to understand about aqueous solutions.

Undiluted solution has the highest concentration. Follow Equations 1, 2, 3, and 4 to calculate the molarity of permanganate. This value is the undiluted concentration, in which the highest absorbance (_A_) value is observed.

### 3.5 Dilution formula

{% include callout.html content="I just wanted to follow up on my last email. I read the questions page and I am still confused on how the concentration is less than the concentration multiplied by three. Because of the dilution formula where M2=M1V1/V2  wouldn’t the one with the highest volume standard with the lowest volume DI water had the highest value. I am sorry if I am getting confused on something simple here." type="danger" %}

You are applying the dilution formula incorrectly. You should follow the following steps to find and plug in the correct _V_ values. I am using the second row of your data table.

- V<sub>1</sub> = 30.00 mL of the stock MnO<sub>4</sub><sup>-</sup> solution.
- Add 10.00 mL of DI water.
- Final volume becomes V<sub>2</sub> = 40.00 mL of diluted MnO<sub>4</sub><sup>-</sup> solution.
- In sum, you should plug in the following values:
  - V<sub>1</sub> = 30.00 mL
  - V<sub>2</sub> = 40.00 mL
  - M<sub>1</sub> = 0.0005126 M based on your first row. (Please check this calculation, the concentration value looks too low.)

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
    <td>84.06%</td>
    <td>10.24%</td>
    <td>86.67%</td>
    <td>95.83%</td>
    <td>57.33%</td>
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
    <td>Mass Percent of Mn in Unknown Sample</td>
    <td>Results Table</td>
  </tr> 
  <tr>
    <td>Discussion Prompts</td>
    <td>Calibration Curve</td>
  </tr>
  <tr>
    <td></td>
    <td>Excel Calculations</td>
  </tr>             
</tbody>
</table>