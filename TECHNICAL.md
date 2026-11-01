# Technical notes

This is the technical companion to the [README](README.md). It covers the original theory, the data, the rules
fixed before looking at results, the full set of test statistics and how to reproduce everything. Every table is
in [results/FINDINGS.md](results/FINDINGS.md).

## The original study

Joan Robinson, *The Economics of Imperfect Competition*, London, Macmillan, 1933. Book V, chapters 15 ("Price
Discrimination," pp. 179–202) and 16 ("The Moral of Price Discrimination," pp. 203–208). The book is theory and
reports no data. Its results, checked against the 1933 edition scanned by the Internet Archive, are these.

| Result | Location |
|---|---|
| Marginal value = average value × (e − 1)/e; with e = 2, marginal value is half the average | p. 36 |
| Monopoly price = marginal cost × e/(e − 1) | p. 64 |
| Discrimination needs separable markets and market power; under perfect competition it "could not exist" | pp. 179–180 |
| Marginal revenue is equalized across markets; prices ranked inversely to elasticities | pp. 181–187 |
| With straight-line demands, output is the same as under a single price (credited to Pigou) | pp. 189–192 |
| Output rises or falls with the "adjusted concavity" of the more elastic demand curve | pp. 193–194 |
| Discrimination can make an otherwise unprofitable product viable; output is the welfare test | pp. 203–206 |

The theory's sharpest testable prediction is the first clause of pp. 179–180. The gap between prices charged to
separable groups should widen with the seller's market power and vanish under competition.

## Headline results

| Test | Estimate | Standard error | N |
|---|---|---|---|
| Discount on log admission rate, private nonprofit, with endowment, sticker price, state | −0.166 | 0.009 | 793 |
| Same, public in-state | −0.083 | 0.021 | 481 |
| Same, private, discount net of maximum Pell | −0.186 | 0.008 | 793 |
| 568-case defendants vs other privates admitting under 15% (adjusted) | +0.046 | 0.021 | 45 |
| Pell share on discount net of Pell, private, full controls | −17.7 | 4.4 | 793 |
| Log Pell recipients on discount net of Pell, private, full controls | −0.23 | 0.26 | 793 |
| Log first-year class on discount net of Pell, private, full controls | +0.62 | 0.29 | 793 |

Median income discount at private nonprofits ranges from 0.93 (admission rate under 10%) to 0.26 (open admission);
for-profit colleges at open or near-open admission have a median of 0.16, and 0.00 once the maximum Pell Grant is
added back.

## Data

All files are IPEDS complete data files from the National Center for Education Statistics
(https://nces.ed.gov/ipeds/datacenter/DataFiles.aspx), downloaded November 1, 2026, committed as zips in
`data/raw/ipeds/`. Where a zip holds a revised file (`*_rv.csv`) the scripts use it.

| File | Contents used |
|---|---|
| `SFA2223.zip` | Average net price by income bracket for Title IV first-time full-time students, 2020–21 to 2022–23 (`NPIS4bY` public in-state, `NPT4bY` private); bracket counts (`GIS4Nb2`, `GRN4Nb2`); Pell share and count (`PGRNT_P`, `PGRNT_N`); first-time full-time cohort (`SCUGFFN`) |
| `ADM2022.zip` | Applicants, admissions, enrollees, fall 2022 (`APPLCN`, `ADMSSN`, `ENRLT`) |
| `IC2022.zip` | Open-admission flag (`OPENADMP`) |
| `HD2022.zip` | Name, state, control, level, degree-granting and active flags |
| `DRVIC2022.zip` | Total price, in-state, on campus (`CINSON`), off campus as fallback |
| `DRVF2023.zip` | Endowment per FTE (`F1ENDMFT` for publics and `F2ENDMFT` for privates, each falling back to the other form when a college files on it) |

The maximum Pell Grant for 2022–23, $6,895, is from Federal Student Aid Dear Colleague Letter GEN-22-04.

## Method

Rules fixed before seeing results:

- Four-year, degree-granting, active institutions; public, private nonprofit and for-profit.
- Each bracket price is the median of the three published years, and needs at least two of them.
- At least 10 Title IV first-time students in both the $0–30,000 and over-$110,000 brackets in 2022–23.
- Selectivity tiers by admission rate (under 10%, 10–25%, 25–50%, 50–75%, 75% or more); open-admission schools
  without admissions data form their own tier.
- Each discount measure is winsorized at its own 1st and 99th percentiles for regressions only; tables use raw
  medians.
- The named-schools list and the 568 defendant list were written before the data were merged.

The income discount and its Pell-adjusted version are

```math
D_i = 1 - \frac{P_{i,\text{low}}}{P_{i,\text{high}}}, \qquad D_i^{\text{ex Pell}} = 1 - \frac{\min(P_{i,\text{low}} + 6{,}895,\ P_{i,\text{high}})}{P_{i,\text{high}}}
```

The discrimination test, run separately for private nonprofit and public colleges, with HC1 robust standard errors:

```math
\begin{aligned}
D_i &= \alpha + \beta \ln A_i + \gamma_1 \ln(1 + E_i) + \gamma_2 \ln S_i + \delta_{s(i)} + \varepsilon_i \\
H_0&: \beta = 0 \qquad H_1 \text{ (Robinson)}: \beta < 0
\end{aligned}
```

Here *A* is the admission rate, *E* endowment per FTE, *S* the sticker price and δ a state effect. The output test
puts the discount on the right:

```math
\begin{aligned}
Y_i &= \alpha + \theta D_i + \beta \ln A_i + \gamma_1 \ln(1 + E_i) + \gamma_2 \ln S_i + \delta_{s(i)} + u_i \\
H_0&: \theta = 0 \qquad \text{output in the weaker market rises if } \theta > 0
\end{aligned}
```

with *Y* the Pell share (percentage points), the log number of Pell recipients, or the log first-year full-time
class. The 568 comparison regresses the discount on a defendant indicator, log admission rate and log endowment per
FTE among private nonprofits admitting under 15% (17 defendants, 28 others).

## Full test statistics

Discount regressions (`results/regressions_discount.csv`), coefficient on log admission rate:

| Sample | Outcome | Admit only | + endowment, sticker | + state | + yield |
|---|---|---|---|---|---|
| Private | Discount | −0.226 (0.007) | −0.158 (0.009) | −0.166 (0.009) | −0.155 (0.014) |
| Private | Net of Pell | −0.263 (0.008) | −0.180 (0.008) | −0.186 (0.008) | −0.164 (0.012) |
| Public | Discount | −0.151 (0.021) | −0.146 (0.022) | −0.083 (0.021) | −0.074 (0.024) |
| Public | Net of Pell | −0.170 (0.022) | −0.135 (0.019) | −0.088 (0.016) | −0.082 (0.018) |

All p-values are below 0.003. Output regressions (`results/regressions_output.csv`), full controls, coefficient on
the discount net of Pell (on the raw discount in brackets):

| Sample | Pell share | Log Pell recipients | Log first-year class |
|---|---|---|---|
| Private | −17.7 (4.4) [−9.8 (4.0)] | −0.23 (0.26) [−0.21 (0.23)] | 0.62 (0.29) [0.26 (0.26)] |
| Public | −27.2 (5.9) [−5.9 (6.5)] | 0.10 (0.48) [−0.03 (0.39)] | 0.98 (0.48) [0.29 (0.37)] |

## Reproducing the results

```bash
pip install -r requirements.txt
python src/robinson_tuition.py
python src/output_test.py
```

The first script builds `results/sample_colleges.csv` and the discrimination tables and figures; the second reads
that file. Both run offline from the committed zips in a few seconds.

## Repository layout

| Path | What it is |
|---|---|
| `src/robinson_tuition.py` | Sample, discount tables, regressions, open-access and 568 comparisons, named schools, two figures |
| `src/output_test.py` | Robinson's output question: Pell share, Pell count and class size against the discount |
| `results/FINDINGS.md` | Plain-English summary and every table |
| `data/raw/ipeds/` | IPEDS zips |

## References

- Robinson, J. (1933). *The Economics of Imperfect Competition*. London, Macmillan.
- Chamberlin, E. H. (1933). *The Theory of Monopolistic Competition*. Harvard University Press.
- Pigou, A. C. (1920). *The Economics of Welfare*. London, Macmillan.
- Schmalensee, R. (1981). Output and welfare implications of monopolistic third-degree price discrimination.
  *American Economic Review* 71(1).
- Varian, H. R. (1985). Price discrimination and social welfare. *American Economic Review* 75(4).
- US Department of Education, Federal Student Aid (2022). Dear Colleague Letter GEN-22-04, revised 2022–2023
  Federal Pell Grant payment and disbursement schedules.
- *Henry v. Brown University*, No. 1:22-cv-00125 (N.D. Ill., filed January 9, 2022).
