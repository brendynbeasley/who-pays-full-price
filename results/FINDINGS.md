# Robinson (1933) on American college prices: findings

## In plain English

Joan Robinson showed in 1933 that a seller who can split its buyers into groups charges the most to the group least
sensitive to price, and that it can only do so if it has market power. US colleges publish what families in five
income groups pay, which makes them a clean test.

- **Market power and price gaps go together.** The 26 private colleges admitting under 10% of applicants, among
  them Harvard, Princeton, Yale and Duke, charge their poorest aided families a median of $3,344 a year and their
  richest $47,066. Private colleges admitting most applicants charge about $18,600 and $28,000.
- **Sellers without market power barely discriminate.** At open or near-open admission, for-profit colleges such as
  Grand Canyon and Full Sail charge their poorest families about what they charge their richest once the federal
  Pell Grant is counted. Southern New Hampshire and Liberty, both nonprofits, are close to one price too.
- **The 568-case universities are not unusually stingy.** The 17 universities sued in 2022 over shared aid
  formulas, from MIT and Yale to Vanderbilt and Penn, discount slightly more steeply than other highly selective
  private colleges.
- **Steeper discounts have not brought in more low-income students.** Colleges that discount more by income enroll
  a smaller share of Pell recipients and no more of them in number, so Robinson's case for discrimination, that it
  serves buyers a single price would lose, does not show up in these data.

The [README](../README.md) tells the story; [TECHNICAL.md](../TECHNICAL.md) has the method.

**Key to the labels.** *Price 0–30k* and *price over 110k* are average annual net prices (cost of attendance minus
all grants) for first-time, full-time freshmen receiving federal aid, in the lowest and highest family-income
brackets, taken as the median of 2020–21, 2021–22 and 2022–23. *Discount* is 1 − price 0–30k ÷ price over 110k.
*Discount ex Pell* adds the 2022–23 maximum Pell Grant ($6,895) to the low price first. *Pell share* is the percent of
full-time first-time freshmen receiving a Pell Grant. *Admit rate* is fall 2022 admissions ÷ applicants. Public
colleges are measured at in-state prices. Dollar figures are nominal.

## Sample

1,457 four-year colleges (832 private nonprofit, 593 public, 32 for-profit) out of 2,840 active four-year
degree-granting institutions. 398 had no 2022–23 aid record, 651 lacked a full set of bracket prices in at least two
of three years, and 334 had fewer than 10 aided freshmen in the lowest or highest bracket.

## Income discount by selectivity (`discount_by_tier.csv`)

| control | admit rate tier | colleges | price 0–30k | price over 110k | gap | discount | discount ex Pell | Pell share |
|---|---|---|---|---|---|---|---|---|
| Public (in-state) | Under 10% | 1 | 6,864 | 30,301 | 23,437 | 0.773 | 0.546 | 26.0 |
| Public (in-state) | 10–25% | 8 | 7,220 | 28,076 | 21,636 | 0.759 | 0.514 | 20.5 |
| Public (in-state) | 25–50% | 35 | 7,322 | 22,977 | 12,268 | 0.671 | 0.292 | 25.0 |
| Public (in-state) | 50–75% | 114 | 10,349 | 20,687 | 10,514 | 0.510 | 0.181 | 38.0 |
| Public (in-state) | 75% or more | 333 | 10,918 | 20,313 | 9,696 | 0.473 | 0.139 | 39.0 |
| Public (in-state) | Open admission | 102 | 7,397 | 13,716 | 6,611 | 0.469 | 0.000 | 44.0 |
| Public (in-state) | All | 593 | 10,045 | 19,687 | 9,154 | 0.489 | 0.126 | 39.0 |
| Private nonprofit | Under 10% | 26 | 3,344 | 47,066 | 43,587 | 0.926 | 0.773 | 19.0 |
| Private nonprofit | 10–25% | 37 | 10,988 | 48,971 | 39,262 | 0.788 | 0.642 | 16.0 |
| Private nonprofit | 25–50% | 66 | 17,516 | 39,631 | 17,697 | 0.433 | 0.237 | 20.0 |
| Private nonprofit | 50–75% | 277 | 18,857 | 28,028 | 8,268 | 0.297 | 0.053 | 34.0 |
| Private nonprofit | 75% or more | 395 | 18,598 | 28,070 | 8,811 | 0.327 | 0.070 | 36.0 |
| Private nonprofit | Open admission | 31 | 16,337 | 22,727 | 6,196 | 0.256 | 0.000 | 50.0 |
| Private nonprofit | All | 832 | 18,194 | 28,964 | 9,105 | 0.334 | 0.079 | 33.0 |
| For-profit | 25–50% | 3 | 29,220 | 34,794 | 8,471 | 0.183 | 0.034 | 49.0 |
| For-profit | 50–75% | 4 | 17,300 | 24,080 | 9,800 | 0.371 | 0.122 | 57.0 |
| For-profit | 75% or more | 8 | 27,904 | 31,688 | 5,391 | 0.171 | 0.000 | 40.5 |
| For-profit | Open admission | 17 | 23,910 | 28,121 | 5,436 | 0.163 | 0.000 | 70.0 |
| For-profit | All | 32 | 23,930 | 28,884 | 5,581 | 0.173 | 0.000 | 56.5 |

All entries are medians across colleges. The median net price for each of the five brackets, by control and tier,
is in `price_ladder.csv` and `price_ladder.png`.

## Regressions of the discount on admission rate (`regressions_discount.csv`)

Coefficient on log admission rate, HC1 standard errors in parentheses. *Halving* is the implied change in the
discount when the admission rate halves (−β × ln 2).

| sample | outcome | spec | N | β | 95% CI | halving | R² |
|---|---|---|---|---|---|---|---|
| Private | discount | admit only | 793 | −0.226 (0.007) | [−0.240, −0.212] | 0.157 | 0.473 |
| Private | discount | + endowment, sticker | 793 | −0.158 (0.009) | [−0.176, −0.140] | 0.109 | 0.561 |
| Private | discount | + endowment, sticker, state | 793 | −0.166 (0.009) | [−0.184, −0.147] | 0.115 | 0.637 |
| Private | discount | + yield, endowment, sticker, state | 793 | −0.155 (0.014) | [−0.182, −0.127] | 0.107 | 0.638 |
| Private | discount ex Pell | admit only | 793 | −0.263 (0.008) | [−0.277, −0.248] | 0.182 | 0.580 |
| Private | discount ex Pell | + endowment, sticker | 793 | −0.180 (0.008) | [−0.196, −0.165] | 0.125 | 0.715 |
| Private | discount ex Pell | + endowment, sticker, state | 793 | −0.186 (0.008) | [−0.202, −0.170] | 0.129 | 0.761 |
| Private | discount ex Pell | + yield, endowment, sticker, state | 793 | −0.164 (0.012) | [−0.187, −0.140] | 0.113 | 0.765 |
| Public | discount | admit only | 481 | −0.151 (0.021) | [−0.192, −0.111] | 0.105 | 0.101 |
| Public | discount | + endowment, sticker | 481 | −0.146 (0.022) | [−0.189, −0.102] | 0.101 | 0.110 |
| Public | discount | + endowment, sticker, state | 481 | −0.083 (0.021) | [−0.125, −0.041] | 0.058 | 0.524 |
| Public | discount | + yield, endowment, sticker, state | 481 | −0.074 (0.024) | [−0.120, −0.027] | 0.051 | 0.525 |
| Public | discount ex Pell | admit only | 481 | −0.170 (0.022) | [−0.212, −0.127] | 0.118 | 0.138 |
| Public | discount ex Pell | + endowment, sticker | 481 | −0.135 (0.019) | [−0.172, −0.099] | 0.094 | 0.300 |
| Public | discount ex Pell | + endowment, sticker, state | 481 | −0.088 (0.016) | [−0.120, −0.056] | 0.061 | 0.637 |
| Public | discount ex Pell | + yield, endowment, sticker, state | 481 | −0.082 (0.018) | [−0.116, −0.047] | 0.057 | 0.638 |

## Open and near-open admission colleges, by control (`open_access_by_control.csv`)

| control | colleges | discount | discount ex Pell | gap | price over 110k |
|---|---|---|---|---|---|
| Public (in-state) | 435 | 0.472 | 0.099 | 8,671 | 19,478 |
| Private nonprofit | 426 | 0.322 | 0.059 | 8,617 | 27,908 |
| For-profit | 25 | 0.163 | 0.000 | 5,436 | 29,646 |

## The 568-case defendants (`case_568.csv`, `case_568_schools.csv`)

Private nonprofits admitting under 15% of applicants. The adjusted difference is the coefficient on a defendant
indicator in a regression of the discount on that indicator, log admission rate and log(1 + endowment per FTE), HC1
errors.

| group | colleges | median admit rate | price 0–30k | price over 110k | median discount | mean discount | median endowment per FTE |
|---|---|---|---|---|---|---|---|
| Other private, admit under 15% | 28 | 0.110 | 5,798 | 49,131 | 0.87 | 0.84 | 447,313 |
| 568-case defendants | 17 | 0.065 | 3,393 | 47,835 | 0.93 | 0.93 | 708,663 |

Adjusted difference 0.046 (0.021), p = 0.029, N = 45. All 17 defendants are in the sample; the school-level list
with each discount is `case_568_schools.csv`.

## Named schools (`named_schools.csv`)

| school | control | admit rate | sticker price | price 0–30k | price 48–75k | price over 110k | discount | Pell share | price 0–30k, 2022–23 only |
|---|---|---|---|---|---|---|---|---|---|
| Massachusetts Institute of Technology | Private | 0.040 | 79,850 | −4,129 | 1,918 | 44,726 | 1.092 | 18 | −4,129 |
| Stanford University | Private | 0.037 | 82,162 | −79 | 3,637 | 49,457 | 1.002 | 20 | −79 |
| Yale University | Private | 0.046 | 85,120 | 1,717 | 5,283 | 45,628 | 0.962 | 20 | 28,132 |
| Harvard University | Private | 0.032 | 83,538 | 2,895 | 2,167 | 52,634 | 0.945 | 21 | 2,895 |
| Duke University | Private | 0.063 | 82,749 | 3,295 | 10,076 | 49,945 | 0.934 | 11 | 3,295 |
| Princeton University | Private | 0.057 | 80,415 | 2,841 | 6,975 | 39,943 | 0.929 | 19 | 2,518 |
| Vanderbilt University | Private | 0.067 | 84,412 | 5,797 | 8,892 | 43,288 | 0.866 | 22 | 5,797 |
| University of Michigan-Ann Arbor | Public | 0.177 | 33,556 | 4,926 | 11,621 | 27,199 | 0.819 | 18 | 4,926 |
| University of California-Los Angeles | Public | 0.086 | 36,980 | 6,864 | 11,065 | 30,301 | 0.773 | 26 | 6,864 |
| University of Southern California | Private | 0.120 | 85,064 | 12,880 | 18,993 | 52,817 | 0.756 | 20 | 15,470 |
| Ohio State University-Main Campus | Public | 0.527 | 30,185 | 6,956 | 13,620 | 26,186 | 0.734 | 17 | 6,259 |
| New York University | Private | 0.125 | 82,095 | 16,816 | 18,555 | 58,906 | 0.715 | 22 | 16,816 |
| Arizona State University Campus Immersion | Public | 0.898 | 31,127 | 8,909 | 15,308 | 20,904 | 0.574 | 29 | 8,909 |
| The University of Texas at Austin | Public | 0.314 | 30,246 | 12,157 | 17,258 | 28,408 | 0.572 | 27 | 12,972 |
| Pennsylvania State University-Main Campus | Public | 0.552 | 39,447 | 20,135 | 27,137 | 36,340 | 0.446 | 13 | 19,458 |
| Grand Canyon University | For-profit | 0.779 | 32,100 | 18,207 | 21,977 | 23,879 | 0.238 | 30 | 18,474 |
| Southern New Hampshire University | Private | 0.964 | 37,280 | 31,967 | 33,040 | 35,345 | 0.096 | 61 | 33,202 |
| Liberty University | Private | 0.993 | 42,498 | 30,398 | 27,214 | 31,028 | 0.020 | 30 | 30,504 |
| Full Sail University | For-profit | open | 42,157 | 29,893 | 28,856 | 30,479 | 0.019 | 70 | 31,667 |

The last column shows why the three-year median is used. Yale's 2022–23 entry for its poorest families is far out of
line with its other two years.

## Output: Pell share by discount third (`output_by_discount_tercile.csv`)

Private nonprofits, split into thirds by the discount ex Pell within each admission tier (ties broken by the raw
discount). Medians.

| admit rate tier | discount third | colleges | discount ex Pell | Pell share | first-year class | price 0–30k |
|---|---|---|---|---|---|---|
| Under 10% | Lowest | 9 | 0.707 | 16.0 | 1,201 | 5,900 |
| Under 10% | Middle | 8 | 0.773 | 19.0 | 1,636 | 3,344 |
| Under 10% | Highest | 9 | 0.827 | 19.0 | 1,406 | 718 |
| 10–25% | Lowest | 13 | 0.497 | 16.0 | 619 | 17,790 |
| 10–25% | Middle | 12 | 0.646 | 15.5 | 1,110 | 11,007 |
| 10–25% | Highest | 12 | 0.747 | 15.5 | 613 | 5,109 |
| 25–50% | Lowest | 22 | 0.000 | 35.0 | 248 | 18,562 |
| 25–50% | Middle | 22 | 0.237 | 20.0 | 453 | 20,350 |
| 25–50% | Highest | 22 | 0.555 | 13.0 | 643 | 13,825 |
| 50–75% | Lowest | 93 | 0.000 | 40.0 | 230 | 19,709 |
| 50–75% | Middle | 92 | 0.053 | 33.5 | 319 | 19,745 |
| 50–75% | Highest | 92 | 0.239 | 24.0 | 439 | 15,687 |
| 75% or more | Lowest | 132 | 0.000 | 39.5 | 296 | 20,249 |
| 75% or more | Middle | 131 | 0.070 | 37.0 | 379 | 19,186 |
| 75% or more | Highest | 132 | 0.194 | 31.5 | 394 | 17,245 |
| Open admission | Lowest | 11 | 0.000 | 50.0 | 175 | 21,090 |
| Open admission | Middle | 10 | 0.000 | 56.5 | 310 | 16,167 |
| Open admission | Highest | 10 | 0.070 | 38.0 | 330 | 14,864 |

## Output regressions (`regressions_output.csv`)

Coefficient on the discount (θ), HC1 errors. *Full controls* means log admission rate, log(1 + endowment per FTE),
log sticker price and state effects. Pell share is in percentage points, so −17.7 means a 10-point steeper discount
goes with a Pell share 1.77 points lower.

| sample | outcome | regressor | raw | + selectivity | full controls |
|---|---|---|---|---|---|
| Private | Pell share | discount ex Pell | −36.9 (1.7) | −38.9 (3.2) | −17.7 (4.4) |
| Private | Pell share | discount | −32.3 (2.1) | −24.3 (3.7) | −9.8 (4.0) |
| Private | log Pell recipients | discount ex Pell | 0.20 (0.13) | 0.14 (0.18) | −0.23 (0.26) |
| Private | log Pell recipients | discount | 0.11 (0.14) | −0.05 (0.18) | −0.21 (0.23) |
| Private | log first-year class | discount ex Pell | 1.57 (0.13) | 1.52 (0.20) | 0.62 (0.29) |
| Private | log first-year class | discount | 1.31 (0.15) | 0.82 (0.21) | 0.26 (0.26) |
| Public | Pell share | discount ex Pell | −26.8 (4.4) | −23.9 (5.3) | −27.2 (5.9) |
| Public | Pell share | discount | −9.3 (5.6) | −4.6 (6.4) | −5.9 (6.5) |
| Public | log Pell recipients | discount ex Pell | 1.26 (0.33) | 0.87 (0.36) | 0.10 (0.48) |
| Public | log Pell recipients | discount | 1.04 (0.31) | 0.68 (0.32) | −0.03 (0.39) |
| Public | log first-year class | discount ex Pell | 2.11 (0.33) | 1.56 (0.36) | 0.98 (0.48) |
| Public | log first-year class | discount | 1.38 (0.31) | 0.83 (0.32) | 0.29 (0.37) |

N = 793 private and 481 public in every row. Full p-values and confidence intervals are in the CSV.

## Figures

- `discount_vs_admit.png` plots each college's income discount against its admission rate, by control.
- `price_ladder.png` shows the median net price across the five income brackets for private colleges by
  selectivity tier, and for for-profits.
- `output_pell_vs_discount.png` plots the Pell share against the discount ex Pell for private colleges, binned within
  three selectivity groups.
