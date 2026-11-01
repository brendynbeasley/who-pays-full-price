"""Robinson (1933) on American college prices: does price discrimination rise with market power?

Joan Robinson's theory of third-degree price discrimination says a seller who can split
buyers into groups that cannot resell to each other charges the highest price in the least
elastic market and the lowest price in the most elastic one, and that a seller facing close
competition cannot sustain much of a gap at all (Economics of Imperfect Competition, ch. 15).

US colleges sell one product (a year of undergraduate study) to families whose incomes they
verify through federal aid forms, and the Department of Education publishes the average net
price each school charges to five family-income groups. This script:

    1. builds the sample of four-year colleges from IPEDS (2022-23 aid year, fall 2022
       admissions, fiscal 2023 finance),
    2. measures each school's "income discount", 1 - P(poorest) / P(richest),
    3. tabulates it by selectivity tier and by control (public, private nonprofit, for-profit),
       which is Robinson's prediction that discrimination needs market power,
    4. runs regressions of the discount on admission rate with wealth and price controls,
    5. compares the 17 universities named in the 2022 "568 cartel" lawsuit with other
       highly selective private universities, and
    6. writes a table of well-known schools and two figures.

The output test (Robinson's chapter 15, section 5) is in src/output_test.py and reads the
sample file this script writes.

Run from the repository root:
    python src/robinson_tuition.py
"""

import zipfile
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "ipeds"
OUT = ROOT / "results"

# Judgment calls, fixed before looking at results
MIN_BRACKET_N = 10        # Title IV first-time students in each end bracket, 2022-23 (noise floor)
MIN_YEARS = 2             # a bracket price needs at least 2 of the 3 published years
WINSOR = (0.01, 0.99)     # winsorize the discount for regressions only
MAX_PELL_2223 = 6895      # maximum Pell Grant, 2022-23 award year (FSA Dear Colleague Letter GEN-22-04)
TIERS = [0, 0.10, 0.25, 0.50, 0.75, 1.0001]
TIER_LABELS = ["Under 10%", "10-25%", "25-50%", "50-75%", "75% or more"]
OPEN_LABEL = "Open admission"
CONTROL = {1: "Public (in-state)", 2: "Private nonprofit", 3: "For-profit"}
BRACKETS = ["$0-30k", "$30-48k", "$48-75k", "$75-110k", "Over $110k"]

# Defendants in Henry v. Brown University, No. 1:22-cv-00125 (N.D. Ill.), the "568 cartel" case
CASE_568 = [
    "Brown University", "California Institute of Technology", "University of Chicago",
    "Columbia University in the City of New York", "Cornell University", "Dartmouth College",
    "Duke University", "Emory University", "Georgetown University", "Johns Hopkins University",
    "Massachusetts Institute of Technology", "Northwestern University", "University of Notre Dame",
    "University of Pennsylvania", "Rice University", "Vanderbilt University", "Yale University",
]

# Schools for the table of names, chosen for recognizability before seeing their numbers
NAMES = [
    "Harvard University", "Princeton University", "Massachusetts Institute of Technology",
    "Stanford University", "Yale University", "Duke University", "Vanderbilt University",
    "New York University", "University of Southern California", "University of Michigan-Ann Arbor",
    "University of California-Los Angeles", "The University of Texas at Austin",
    "Ohio State University-Main Campus", "Pennsylvania State University-Main Campus",
    "Arizona State University Campus Immersion", "Liberty University",
    "Southern New Hampshire University", "Grand Canyon University", "Full Sail University",
]


def read_ipeds(stem, usecols=None):
    """Read one IPEDS zip, preferring the revised (_rv) file when the zip has one."""
    with zipfile.ZipFile(RAW / f"{stem}.zip") as z:
        names = z.namelist()
        rv = [n for n in names if n.endswith("_rv.csv")]
        name = rv[0] if rv else [n for n in names if n.endswith(".csv")][0]
        with z.open(name) as f:
            df = pd.read_csv(f, encoding="latin1", low_memory=False)
    df.columns = [c.strip().upper() for c in df.columns]
    if usecols:
        df = df[usecols]
    print(f"Loaded {stem} ({name}): {len(df):,} rows")
    return df


def bracket_prices(sfa, control):
    """Median of the three published years for each income bracket (robust to one bad year)."""
    out = pd.DataFrame(index=sfa.index)
    for b in range(1, 6):
        pub = sfa[[f"NPIS4{b}{y}" for y in (0, 1, 2)]].to_numpy(dtype=float)
        prv = sfa[[f"NPT4{b}{y}" for y in (0, 1, 2)]].to_numpy(dtype=float)
        vals = pd.DataFrame(np.where((control == 1).to_numpy()[:, None], pub, prv))
        n_years = vals.notna().sum(axis=1).to_numpy()
        med = vals.median(axis=1, skipna=True).to_numpy()
        out[f"p{b}"] = np.where(n_years >= MIN_YEARS, med, np.nan)
        vals = vals.to_numpy()
        out[f"p{b}_2223"] = vals[:, 2]
        cnt_pub = sfa[f"GIS4N{b}2"].astype(float)
        cnt_prv = sfa[f"GRN4N{b}2"].astype(float)
        out[f"n{b}"] = np.where(control == 1, cnt_pub, cnt_prv)
    out["n_all"] = np.where(control == 1, sfa["GIS4N2"].astype(float), sfa["GRN4N2"].astype(float))
    return out


def build_sample():
    hd = read_ipeds("HD2022", ["UNITID", "INSTNM", "STABBR", "CONTROL", "ICLEVEL", "DEGGRANT", "CYACTIVE"])
    ic = read_ipeds("IC2022", ["UNITID", "OPENADMP"])
    adm = read_ipeds("ADM2022", ["UNITID", "APPLCN", "ADMSSN", "ENRLT"])
    drvic = read_ipeds("DRVIC2022", ["UNITID", "CINSON", "CINSOFF"])
    drvf = read_ipeds("DRVF2023", ["UNITID", "F1ENDMFT", "F2ENDMFT"])
    sfa = read_ipeds("SFA2223")

    d = hd[(hd.ICLEVEL == 1) & (hd.DEGGRANT == 1) & (hd.CYACTIVE == 1) & hd.CONTROL.isin([1, 2, 3])]
    print(f"Four-year, degree-granting, active institutions: {len(d):,} of {len(hd):,}")
    d = d.merge(sfa, on="UNITID", how="inner")
    print(f"  with a 2022-23 student financial aid record: {len(d):,}")
    d = d.reset_index(drop=True)
    d = pd.concat([d[["UNITID", "INSTNM", "STABBR", "CONTROL", "PGRNT_P", "PGRNT_N", "SCUGFFN"]],
                   bracket_prices(d, d.CONTROL)], axis=1)
    for frame in (ic, adm, drvic, drvf):
        for c in frame.columns:
            if c != "UNITID":
                frame[c] = pd.to_numeric(frame[c], errors="coerce")
        d = d.merge(frame, on="UNITID", how="left")

    has_prices = d[[f"p{b}" for b in range(1, 6)]].notna().all(axis=1) & (d.p5 > 0)
    print(f"  dropped {(~has_prices).sum():,} without all five bracket prices in 2+ years (or top price <= 0)")
    d = d[has_prices]
    big = (d.n1 >= MIN_BRACKET_N) & (d.n5 >= MIN_BRACKET_N)
    print(f"  dropped {(~big).sum():,} with fewer than {MIN_BRACKET_N} Title IV students in the "
          f"lowest or highest income bracket")
    d = d[big].copy()

    d["control"] = d.CONTROL.map(CONTROL)
    d["discount"] = 1 - d.p1 / d.p5
    d["gap"] = d.p5 - d.p1
    d["discount_ex_pell"] = 1 - (d.p1 + MAX_PELL_2223).clip(upper=d.p5) / d.p5
    d["admit_rate"] = d.ADMSSN / d.APPLCN
    d["yield_rate"] = d.ENRLT / d.ADMSSN
    d["sticker"] = d.CINSON.where(d.CINSON > 0, d.CINSOFF)
    # GASB form (F1) for publics and FASB form (F2) for privates; some publics file FASB, so fall back
    d["endow_fte"] = np.where(d.CONTROL == 1, d.F1ENDMFT.fillna(d.F2ENDMFT), d.F2ENDMFT.fillna(d.F1ENDMFT))
    d["lowinc_share"] = d.n1 / d.n_all
    d["tier"] = pd.cut(d.admit_rate, TIERS, labels=TIER_LABELS).astype(object)
    d.loc[d.tier.isna() & (d.OPENADMP == 1), "tier"] = OPEN_LABEL
    d["case_568"] = d.INSTNM.isin(CASE_568)
    print(f"Final sample: {len(d):,} colleges")
    print(d.groupby("control").size().to_string())
    print(f"  of which {d.tier.isna().sum()} have no admissions data and no open-admission flag "
          f"(kept in totals, left out of tier tables)")
    found = d.INSTNM[d.case_568].tolist()
    print(f"568-case defendants found in sample: {len(found)} of {len(CASE_568)}")
    return d


def tier_table(d):
    rows = []
    order = TIER_LABELS + [OPEN_LABEL]
    for ctrl in CONTROL.values():
        for tier in order:
            g = d[(d.control == ctrl) & (d.tier == tier)]
            if len(g) == 0:
                continue
            rows.append(dict(control=ctrl, admit_rate_tier=tier, colleges=len(g),
                             median_price_0_30k=g.p1.median(), median_price_over_110k=g.p5.median(),
                             median_gap=g.gap.median(), median_discount=g.discount.median(),
                             median_discount_ex_pell=g.discount_ex_pell.median(),
                             median_pell_share=g.PGRNT_P.median()))
        g = d[d.control == ctrl]
        rows.append(dict(control=ctrl, admit_rate_tier="All", colleges=len(g),
                         median_price_0_30k=g.p1.median(), median_price_over_110k=g.p5.median(),
                         median_gap=g.gap.median(), median_discount=g.discount.median(),
                         median_discount_ex_pell=g.discount_ex_pell.median(),
                         median_pell_share=g.PGRNT_P.median()))
    t = pd.DataFrame(rows)
    t.to_csv(OUT / "discount_by_tier.csv", index=False, float_format="%.3f")
    print("\nIncome discount by selectivity tier (medians):")
    print(t.to_string(index=False, float_format=lambda x: f"{x:,.2f}"))
    return t


def ladder_table(d):
    rows = []
    for (ctrl, tier), g in d.groupby(["control", "tier"]):
        for b in range(1, 6):
            rows.append(dict(control=ctrl, admit_rate_tier=tier, bracket=BRACKETS[b - 1],
                             median_net_price=g[f"p{b}"].median(), colleges=len(g)))
    t = pd.DataFrame(rows)
    t.to_csv(OUT / "price_ladder.csv", index=False, float_format="%.0f")
    return t


def regressions(d):
    rows = []
    # each measure is trimmed at its own 1st and 99th percentiles, as in src/output_test.py
    lo, hi = d.discount.quantile(WINSOR[0]), d.discount.quantile(WINSOR[1])
    lo_xp, hi_xp = d.discount_ex_pell.quantile(WINSOR[0]), d.discount_ex_pell.quantile(WINSOR[1])
    d = d.assign(disc_w=d.discount.clip(lo, hi), disc_xp_w=d.discount_ex_pell.clip(lo_xp, hi_xp))
    specs = {
        "admit only": "{y} ~ np.log(admit_rate)",
        "+ endowment, sticker": "{y} ~ np.log(admit_rate) + np.log1p(endow_fte) + np.log(sticker)",
        "+ endowment, sticker, state": "{y} ~ np.log(admit_rate) + np.log1p(endow_fte) + np.log(sticker) + C(STABBR)",
        "+ yield, endowment, sticker, state": "{y} ~ np.log(admit_rate) + yield_rate + np.log1p(endow_fte) + np.log(sticker) + C(STABBR)",
    }
    for ctrl in ["Private nonprofit", "Public (in-state)"]:
        base = d[(d.control == ctrl) & d.admit_rate.between(0, 1, inclusive="right")
                 & d.endow_fte.notna() & (d.sticker > 0) & d.yield_rate.notna()]
        for y, ylab in [("disc_w", "discount"), ("disc_xp_w", "discount net of max Pell")]:
            for name, f in specs.items():
                m = smf.ols(f.format(y=y), data=base).fit(cov_type="HC1")
                b = m.params["np.log(admit_rate)"]
                rows.append(dict(control=ctrl, outcome=ylab, spec=name, n=int(m.nobs),
                                 coef_log_admit=b, se=m.bse["np.log(admit_rate)"],
                                 p=m.pvalues["np.log(admit_rate)"],
                                 ci_low=m.conf_int().loc["np.log(admit_rate)", 0],
                                 ci_high=m.conf_int().loc["np.log(admit_rate)", 1],
                                 effect_of_halving_admit=-b * np.log(2), r2=m.rsquared))
    t = pd.DataFrame(rows)
    t.to_csv(OUT / "regressions_discount.csv", index=False, float_format="%.6f")
    print("\nDiscount on log admission rate (HC1 errors):")
    print(t.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    return t


def competition_test(d):
    """Robinson p. 180: competing sellers cannot sustain much of a gap. Same open-access market,
    different objectives: for-profit vs nonprofit colleges at open or near-open admission."""
    g = d[d.tier.isin([OPEN_LABEL, "75% or more"])]
    rows = []
    for ctrl in CONTROL.values():
        h = g[g.control == ctrl]
        rows.append(dict(control=ctrl, colleges=len(h), median_discount=h.discount.median(),
                         median_discount_ex_pell=h.discount_ex_pell.median(),
                         median_gap=h.gap.median(), median_price_over_110k=h.p5.median()))
    t = pd.DataFrame(rows)
    t.to_csv(OUT / "open_access_by_control.csv", index=False, float_format="%.3f")
    print("\nOpen or near-open admission colleges, by control:")
    print(t.to_string(index=False, float_format=lambda x: f"{x:,.3f}"))


def case_568(d):
    """Defendants in the 568 case vs other private nonprofits admitting under 15%."""
    sel = d[(d.control == "Private nonprofit") & (d.admit_rate < 0.15)]
    rows = []
    for flag, h in sel.groupby("case_568"):
        rows.append(dict(group="568-case defendants" if flag else "Other private, admit < 15%",
                         colleges=len(h), median_admit_rate=h.admit_rate.median(),
                         median_price_0_30k=h.p1.median(), median_price_over_110k=h.p5.median(),
                         median_discount=h.discount.median(), mean_discount=h.discount.mean(),
                         median_endow_fte=h.endow_fte.median()))
    t = pd.DataFrame(rows)
    a, b = sel.discount[sel.case_568], sel.discount[~sel.case_568]
    m = smf.ols("discount ~ case_568 + np.log(admit_rate) + np.log1p(endow_fte)",
                data=sel.assign(case_568=sel.case_568.astype(int))).fit(cov_type="HC1")
    t["adj_diff_568"] = m.params["case_568"]
    t["adj_diff_se"] = m.bse["case_568"]
    t["adj_diff_p"] = m.pvalues["case_568"]
    t["adj_n"] = int(m.nobs)
    t.to_csv(OUT / "case_568.csv", index=False, float_format="%.4f")
    print(f"\n568-case comparison (private, admit < 15%): {len(a)} defendants vs {len(b)} others")
    print(t.to_string(index=False, float_format=lambda x: f"{x:,.3f}"))
    sel[["INSTNM", "case_568", "admit_rate", "p1", "p5", "discount", "endow_fte"]].sort_values(
        "discount").to_csv(OUT / "case_568_schools.csv", index=False, float_format="%.3f")


def names_table(d):
    t = d[d.INSTNM.isin(NAMES)].copy()
    missing = sorted(set(NAMES) - set(t.INSTNM))
    print(f"\nNamed schools found: {len(t)} of {len(NAMES)}; not in sample: {missing}")
    t = t[["INSTNM", "control", "admit_rate", "sticker", "p1", "p3", "p5", "discount",
           "PGRNT_P", "lowinc_share", "p1_2223"]].sort_values("discount", ascending=False)
    t.columns = ["school", "control", "admit_rate", "sticker_price", "price_0_30k", "price_48_75k",
                 "price_over_110k", "discount", "pell_share_pct", "lowinc_share", "price_0_30k_2022_23_only"]
    t.to_csv(OUT / "named_schools.csv", index=False, float_format="%.3f")
    print(t.to_string(index=False, float_format=lambda x: f"{x:,.2f}"))


def figures(d):
    colors = {"Private nonprofit": "#2a6f97", "Public (in-state)": "#e07a1f", "For-profit": "#7a7a7a"}
    fig, ax = plt.subplots(figsize=(8, 5.2))
    for ctrl in ["Public (in-state)", "Private nonprofit", "For-profit"]:
        g = d[(d.control == ctrl) & d.admit_rate.notna() & (d.admit_rate > 0)]
        ax.scatter(g.admit_rate * 100, g.discount.clip(-0.2, 1.2), s=9, alpha=0.45,
                   color=colors[ctrl], label=f"{ctrl} ({len(g)})")
    for name, label in [("Harvard University", "Harvard"), ("Princeton University", "Princeton"),
                        ("Pennsylvania State University-Main Campus", "Penn State"),
                        ("Southern New Hampshire University", "SNHU"),
                        ("University of Michigan-Ann Arbor", "Michigan")]:
        r = d[d.INSTNM == name]
        if len(r) and r.admit_rate.notna().all():
            ax.annotate(label, (r.admit_rate.iloc[0] * 100, r.discount.iloc[0]), fontsize=8,
                        xytext=(4, 4), textcoords="offset points")
    ax.set_xscale("log")
    ax.set_xticks([3, 5, 10, 25, 50, 100])
    ax.set_xticklabels(["3%", "5%", "10%", "25%", "50%", "100%"])
    ax.set_xlabel("Admission rate, fall 2022 (log scale; fewer admitted = more market power)")
    ax.set_ylabel(r"Income discount  1 - P(\$0-30k) / P(over \$110k)")
    ax.set_title("The more selective the college, the wider its price gap by family income")
    ax.axhline(0, color="black", lw=0.6)
    ax.legend(frameon=False, fontsize=8, loc="lower left")
    fig.tight_layout()
    fig.savefig(OUT / "discount_vs_admit.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5))
    priv = d[d.control == "Private nonprofit"]
    for tier, col in zip(TIER_LABELS, ["#08306b", "#2171b5", "#6baed6", "#9ecae1", "#c6dbef"]):
        g = priv[priv.tier == tier]
        ax.plot(BRACKETS, [g[f"p{b}"].median() / 1000 for b in range(1, 6)], marker="o",
                color=col, label=f"Private, admit rate {tier.lower()} ({len(g)})")
    fp = d[d.control == "For-profit"]
    ax.plot(BRACKETS, [fp[f"p{b}"].median() / 1000 for b in range(1, 6)], marker="s",
            color="#7a7a7a", ls="--", label=f"For-profit, all ({len(fp)})")
    ax.set_ylabel("Median net price per year, $ thousands")
    ax.set_xlabel("Family income")
    ax.set_title("What a year costs, by family income and selectivity, 2020-21 to 2022-23")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "price_ladder.png", dpi=150)
    plt.close(fig)


def main():
    OUT.mkdir(exist_ok=True)
    d = build_sample()
    keep = ["UNITID", "INSTNM", "STABBR", "control", "tier", "admit_rate", "yield_rate", "sticker",
            "endow_fte", "p1", "p2", "p3", "p4", "p5", "p1_2223", "p5_2223", "n1", "n5", "n_all",
            "discount", "discount_ex_pell", "gap", "PGRNT_P", "PGRNT_N", "SCUGFFN", "lowinc_share", "case_568"]
    d[keep].to_csv(OUT / "sample_colleges.csv", index=False, float_format="%.4f")
    tier_table(d)
    ladder_table(d)
    regressions(d)
    competition_test(d)
    case_568(d)
    names_table(d)
    figures(d)
    print(f"\nWrote results to {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
