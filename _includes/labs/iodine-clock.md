## 1 Goals

- Determine the general rate law for a chemical reaction by calculating the reaction rate for various concentrations of reactants. 

- Using the concentrations listed on the reagent bottles and the volumes in Table 2, calculate the diluted concentrations for each species using

{% include eq.html file="ykf-1.svg" %} 

- Calculate the reaction rate for each trial using the diluted concentration of thiosulfate and the time (in seconds) it took for the blue complex to appear, using 

{% include eq.html file="ykf-2.svg" %} 

- The partial order of each reactant will be found by comparing different rates and sets of concentrations to one another, yielding the experimental rate law for this specific reaction.

- Use the method of initial rates and logarithms to calculate the partial order of each reactant for the `a` and `b` set of runs separately. e.g. The ratio of `run 2` over `run 1` gives:

{% include eq.html file="ykf-3.svg" %}
 
where _z_ can be found by
 
{% include eq.html file="ykf-4.svg" %}

- This process is then repeated until all of the partial orders in the rate law are determined. The average partial orders should be listed to the same number of significant figures as the individual trial partial orders.

- Calculate the rate constant at that temperature using the rate and concentration data from any run

{% include eq.html file="ykf-5.svg" %}
  
- _k_ value should be calculated for each run, which means (4 runs) x (2 trials) = 8 different _k_ values are calculated. 

- Report average _k_ constant ± standard deviation, following the rules for significant figures.

## 2 Assignment

- Watch the demo video for the experiment
- Download the data set and do the data analysis  
- Upload the __partial lab report__ in the `PDF` format:
  - This is a deviation for the summer session only.
  - Include the following sections: `Abstract`, `Procedures`, `Results`, `Data Table`, `Experimental Rate Law`, and `Discussion` (not a full discussion section; just itemize and answer the questions.)
  - You don't need to include sample calculations in the __partial report__ (it is in Excel only), don't need to write narrative explaining data tables and calculations.
- Upload all calculations and data tables in an MS Excel file 
- You should review the `Lab Report Guidelines`, `Sample General Chemistry Lab Report`, and `Appendix E` on D2L while writing to ensure that your drafts are correctly formatted.

## 3 Q&A Highlights 

### 3.1 Concentrations of the stock solutions

{% include callout.html content="I was only given the concentration for [H<sup>+</sup>]. However I believe that I need the stock concentrations of the other reactants as well in order to be able to calculate the diluted concentration of thiosulfite. Is there something that I am missing about this?" type="danger" %}

Assume that the stock solutions are exactly prepared in the suggested values in Table 1.

<table>
<caption>Table 1. The concentrations of stock solutions.</caption>
<thead>
  <tr>
    <th>Compounds</th>
    <th>Concentration (M)</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>Hydrochloric acid</td>
    <td>0.0500</td>
  </tr>
  <tr>
    <td>Hydrogen peroxide</td>
    <td>0.0500</td>
  </tr>
  <tr>
    <td>Potassium iodide</td>
    <td>0.0500</td>
  </tr>
  <tr>
    <td>Sodium thiosulfate</td>
    <td>0.0100</td>
  </tr>      
</tbody>
</table>

### 3.2 Calculating the initial concentrations

{% include callout.html content="We're supposed to calculate M<sub>2</sub> using data from Table 2. I'm not sure which volume to use with regards to runs since they change for different runs. Do I need to find M<sub>2</sub> of all reactants for all 4 runs? Or do I just need to find M<sub>2</sub> for a specific run? " type="danger" %}

Using the stock concentrations listed in Table 1 and the volumes in Table 2, calculate the diluted concentrations for each species by plugging in the values to Equation 1. These calculated concentrations are known as initial concentrations.

<table>
<caption>Table 2. First row of from the lab manual.</caption>
<thead>
  <tr>
    <th></th>
    <th>Hydrogen peroxide</th>
    <th>Hydrochloric acid</th>
    <th>Potassium iodide</th>
    <th>Sodium thiosulfate</th>
    <th>Water</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>Run 1 volume (mL)</td>
    <td>10.00</td>
    <td>10.00</td>
    <td>10.00</td>
    <td>10.00</td>
    <td>10.00</td>
  </tr>
</tbody>
</table>

For example, the intial concentration of hydrogen peroxide Run 1:

{% include eq.html file="ykf-6.svg" %}

For Run 1, you will do this calculation for all species across the line. These values are the initial concentrations for Run 1. Repeat this calculation for all 4 runs and plug into Equation 3 to find the partial orders of _x_, _y_, and _z_.

_Please note that you are expected to make an Excel table and do all of these individual calculations by using Excel functions._

## 4 Assessment

### 4.1 Misconceptions

#### 4.1.1 Determining partial orders

{% include callout.html content="The partial order of each reactant is the same value of the stoichiometric number or the exponent linked to a particular reactant." type="danger" %}

Incorrect. Partial orders are experimentally determined using the initial concentrations. See Equations 3 and 4 for more details.

{% include callout.html content="If the concentration of HCl were doubled, the reaction time would not change because
thiosulfate is the limiting reactant and therefore the reaction time is dependent upon the
consumption of thiosulfate. The concentration of H<sub>2</sub>O<sub>2</sub> and KI do not effect the reaction
time since the reaction time depends on the consumption of thiosulfate, the limiting
reactant." type="danger" %}

This explanation is based on the following rate law: _rate = k [H<sub>2</sub>O<sub>2</sub>]<sup>1</sup>[HCl]<sup>1</sup>[KI]<sup>1</sup>_. If all partial orders are determined as 1, which is incorrect for this experiment, then every species would affect the reaction rate in the same proportion. e.g. If the concentration of HCl or H<sub>2</sub>O<sub>2</sub> or KI were doubled, the reaction time would be half.

#### 4.1.2 If the concentration of HCl were doubled, how would the reaction time change?

{% include callout.html content="If the concentration of HCl were doubled, the reaction time would increase. The concentration of H<sub>2</sub>O<sub>2</sub> would slow down the reaction time. The concentration of KI would speed up the reaction time." type="danger" %}

{% include callout.html content="This would increase the reaction time because there is more concentration so the reaction
would take longer than it would have originally." type="danger" %}

You would need to base your discussion on the experimental rate law that you discovered. If the species of interest has nonzero partial oder, than you would be able to relate its concentration to the overall reaction rate. 

Please remember that scientific argument is only valid (i.e. viable) if it is based on evidence. Therefore, you must use all the evidences you gathered in this experiment to answer these questions.

Another hint is that the question itself guides you to talk about some species, like H<sub>2</sub>O<sub>2</sub> and KI. 

{% include callout.html content="Increasing any of the concentrations would allow for a faster rate to be observed. The reason behind this is that there are more particles in an increased concentration which allows for more collisions to
happen. This would entail a faster reaction rate." type="danger" %}

The rate law should be experimentally determined to answer this question.

#### 4.1.3 Would you expect the rate constant to change if you heated up the reactants before mixing? 

{% include callout.html content="Yes, the rate constant would change if it were heated up. This would make the heat
constant smaller because the time of the reaction would decrease." type="danger" %}

I see two issues here. 

1. You say that `if the rate constant were heated up`. Well, the rate constant is a concept; you cannot heat it up. Perhaps you meant the reaction vessel was heated up but it was not clear. Again, in a scientific argument we read what you say, as you say it. You have the observations and you have the power to make claims. 

2. You said `the heat constant`. What do you mean? We did not define `heat constant` as a term in this context.

{% include callout.html content="The rate constant would change if the reactants were to be heated up before mixing, the heat would increase the concentration which then would also increase the rate constant." type="danger" %}

Again, there are two issues here:

1. You have no evidence to claim that `the heat would increase the concentration`.
2. Even if so, increasing concentration does not necessarily increase the rate constant. Hint: consider 0<sup>th</sup> order reaction.

#### 4.1.4 How would a wet pipette affect the experimental results?

{% include callout.html content="A wet pipette would change the experimental results in that it would increase the concentrations of the mixtures." type="danger" %}

A wet pipette means that the solution is diluted.

{% include callout.html content="A wet pipette could affect the experimental results significantly by increasing the delivered volume value, therefore making the experimental results inaccurate and inconsistent." type="danger" %}

Disagree. Volume is measured correctly all the time by the use of pipette.

### 4.2 Formatting issues

{% include callout.html content="If the concentration of HCl, H2O2, and KI were doubled the reaction time would also
double (increase)." type="danger" %}

You should use an equation editor to write equations and chemical formulas properly. i.e. I expect to see H<sub>2</sub>O<sub>2</sub> rather than H2O2.

{% include callout.html content=" H202(aq) + 2I-(aq) yields 2 H20(l) + I2(aq)" type="danger" %}

You must use the equation editor for all equations and chemical formulas. So, I expect:

{% include eq.html file="ykf-8.svg" %}
 
### 4.3 Issues with calculations

{% include callout.html content="The overall reaction for Reaction 3 is determined by the sum of x, y and z. The sum is equal to 2.212." type="danger" %}

Although the sum of partial orders can be a fractional number in rare cases, normally at this level you should use general case as whole numbers only. Remember that you learnt only 0<sup>th</sup>, 1<sup>st</sup>, and 2<sup>nd</sup> order reactions. We do not always explicitly say all details but you can use common sense when you do experiments and data analysis.

{% capture content %}
 ...the rate constant being {% include eq.html file="ykf-9.svg" inline=true %}.
{% endcapture %}

{% include callout.html content=content type="danger" %}

There are a few issues:

1. Value and standard deviation do not share a common multiplier, when a multiplier is present.
1. Standard deviation does not have a unit.
2. Rules for significant figures are not followed. 

The expected format is: {% include eq.html file="ykf-10.svg" inline=true %}.

- Standard deviation has 1 sig. fig. (requirement)
- The value has zero decimal place —same as the standard deviation (requirement) 

### 4.4 Feedback

- The PDF file you uploaded: annotations are highlighted with gray background and pink font.
- E-Rubric: D2L will show the rubric with scores and any feedback provided.

### 4.5 Grades

<table>
<caption>Table 3. Grade stats for this experiment.</caption>
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
    <td>76.06%</td>
    <td>8.51%</td>
    <td>73.50%</td>
    <td>95.50%</td>
    <td>61.50%</td>
  </tr>
</tbody>
</table>

### 4.6 Team grading

<table>
<caption>Table 4. Task sharing for team grading based on the sections of the rubric.</caption>
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
    <td>Prelab Assignment</td>
  </tr>
  <tr>
    <td>Discussion</td>
    <td>Postlab Quiz</td>
  </tr>
  <tr>
    <td>Proofreading and General Formatting</td>
    <td>Data Table</td>
  </tr>  
  <tr>
    <td>Experimental Rate Law</td>
    <td>Average Rate Constant</td>
  </tr>
  <tr>
    <td>Discussion Questions</td>
    <td>Excel Calculations</td>
  </tr>         
</tbody>
</table>