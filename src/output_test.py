"""Robinson's output question: does price discrimination let a seller serve the weaker market?

In chapter 15 (section 5) and chapter 16 of The Economics of Imperfect Competition, Robinson
shows that discrimination raises total output when it opens a market that a single price would
leave unserved, leaves output unchanged when demand curves are straight lines, and can lower it
otherwise. Output is also her test of whether discrimination is good for society (p. 206).

For colleges the weaker market is low-income families. This script asks whether colleges that
discount more steeply by income enroll a larger share of Pell Grant recipients (students from
low-income families), and whether they enroll more first-year students in total, holding
selectivity, wealth, sticker price and state constant. It reads results/sample_colleges.csv,
which src/robinson_tuition.py writes, so run that first.

Run from the repository root:
    python src/output_test.py
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results"
WINSOR = (0.01, 0.99)     # same trimming of the discount as the main regressions
TIER_ORDER = ["Under 10%", "10-25%", "25-50%", "50-75%", "75% or more", "Open admission"]


def load():
    d = pd.read_csv(OUT / "sample_colleges.csv")
    print(f"Loaded sample_colleges.csv: {len(d):,} colleges")
    lo, hi = d.discount_ex_pell.quantile(WINSOR[0]), d.discount_ex_pell.quantile(WINSOR[1])
    d["disc_xp_w"] = d.discount_ex_pell.clip(lo, hi)
    lo, hi = d.discount.quantile(WINSOR[0]), d.discount.quantile(WINSOR[1])
    d["disc_w"] = d.discount.clip(lo, hi)
    ok = d.PGRNT_P.notna() & (d.SCUGFFN > 0) & (d.PGRNT_N > 0)
    print(f"  dropped {(~ok).sum()} without a Pell share, a Pell recipient or a first-year cohort count")
    return d[ok].copy()


def order_rank(g):
    """Rank by the Pell-adjusted discount; ties (many are exactly zero) are broken by the raw discount."""
    pos = g.sort_values(["discount_ex_pell", "discount", "UNITID"]).index
    return pd.Series(np.arange(len(g)), index=pos).reindex(g.index)


def binned(d):
    """Pell share by discount tercile within each selectivity tier, private nonprofits."""
    rows = []
    priv = d[d.control == "Private nonprofit"]
    for tier in TIER_ORDER:
        g = priv[priv.tier == tier]
        if len(g) < 15:
            continue
        g = g.assign(tercile=pd.qcut(order_rank(g), 3,
                                     labels=["Lowest third", "Middle third", "Highest third"]))
        for t, h in g.groupby("tercile", observed=True):
            rows.append(dict(admit_rate_tier=tier, discount_tercile=t, colleges=len(h),
                             median_discount_ex_pell=h.discount_ex_pell.median(),
                             median_pell_share=h.PGRNT_P.median(),
                             median_first_year_cohort=h.SCUGFFN.median(),
                             median_price_0_30k=h.p1.median()))
    t = pd.DataFrame(rows)
    t.to_csv(OUT / "output_by_discount_tercile.csv", index=False, float_format="%.3f")
    print("\nPrivate nonprofits: Pell share by discount tercile within selectivity tier")
    print(t.to_string(index=False, float_format=lambda x: f"{x:,.2f}"))
    return t


def regressions(d):
    rows = []
    controls = "np.log(admit_rate) + np.log1p(endow_fte) + np.log(sticker) + C(STABBR)"
    specs = {
        "raw": "{y} ~ {x}",
        "+ selectivity": "{y} ~ {x} + np.log(admit_rate)",
        "+ selectivity, endowment, sticker, state": "{y} ~ {x} + " + controls,
    }
    outcomes = {"PGRNT_P": "Pell share of first-year class (points)",
                "np.log(PGRNT_N)": "log number of first-year Pell recipients",
                "np.log(SCUGFFN)": "log first-year full-time class size"}
    for ctrl in ["Private nonprofit", "Public (in-state)"]:
        base = d[(d.control == ctrl) & (d.admit_rate > 0) & d.endow_fte.notna() & (d.sticker > 0)]
        for y, ylab in outcomes.items():
            for x in ["disc_xp_w", "disc_w"]:
                for name, f in specs.items():
                    m = smf.ols(f.format(y=y, x=x), data=base).fit(cov_type="HC1")
                    rows.append(dict(control=ctrl, outcome=ylab,
                                     regressor="discount net of max Pell" if x == "disc_xp_w" else "discount",
                                     spec=name, n=int(m.nobs), coef=m.params[x], se=m.bse[x],
                                     p=m.pvalues[x], ci_low=m.conf_int().loc[x, 0],
                                     ci_high=m.conf_int().loc[x, 1],
                                     per_10_points=m.params[x] * 0.10, r2=m.rsquared))
    t = pd.DataFrame(rows)
    t.to_csv(OUT / "regressions_output.csv", index=False, float_format="%.6f")
    print("\nOutput regressions (HC1 errors); per_10_points = effect of a 10-point steeper discount")
    print(t.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    return t


def figure(d):
    priv = d[(d.control == "Private nonprofit") & d.tier.notna()]
    groups = {"Admit under 25%": ["Under 10%", "10-25%"], "Admit 25-75%": ["25-50%", "50-75%"],
              "Admit 75%+ or open": ["75% or more", "Open admission"]}
    colors = ["#08306b", "#4292c6", "#9ecae1"]
    fig, ax = plt.subplots(figsize=(8, 5))
    for (label, tiers), col in zip(groups.items(), colors):
        g = priv[priv.tier.isin(tiers)].copy()
        g["bin"] = pd.qcut(order_rank(g), 8, labels=False)
        b = g.groupby("bin").agg(x=("discount_ex_pell", "median"), y=("PGRNT_P", "median"))
        ax.plot(b.x * 100, b.y, marker="o", color=col, label=f"{label} ({len(g)} colleges)")
    ax.set_xlabel("Income discount net of the maximum Pell Grant, percent (median of each eighth)")
    ax.set_ylabel("Share of first-year students with a Pell Grant, %")
    ax.set_title("Private colleges: steeper income discounts, fewer Pell students")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "output_pell_vs_discount.png", dpi=150)
    plt.close(fig)


def main():
    d = load()
    binned(d)
    regressions(d)
    figure(d)
    print(f"\nWrote results to {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
