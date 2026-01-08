#!/usr/bin/env python3
"""
Generate Appendix D Monte Carlo summary table figure from a CSV.

Inputs:
  - figures/AppendixD_monte_carlo_summary_tightened.csv (or path you pass)

Outputs:
  - figures/AppendixD_monte_carlo_summary_table.png (default)
"""
from __future__ import annotations

import argparse
import pandas as pd
import matplotlib.pyplot as plt

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in_csv", default="figures/AppendixD_monte_carlo_summary_tightened.csv")
    ap.add_argument("--out_png", default="figures/AppendixD_monte_carlo_summary_table.png")
    args = ap.parse_args()

    df = pd.read_csv(args.in_csv)

    # Journal-friendly labels (short + wrapped)
    scenario_labels = [
        "Base reality\n(conservative priors; tightened)",
        "Forensic simulation–weighted\npriors (tightened; C_m‑dominant)",
        "Alignment intervention\n(optimistic stress‑test; still C_m‑dominant)",
    ]
    if len(df) == len(scenario_labels):
        df = df.copy()
        df["Scenario"] = scenario_labels

    # Collapse percentiles into compact strings
    out = pd.DataFrame({
        "Scenario": df["Scenario"],
        "log10(C_a)\n[p05, p50, p95]": df.apply(lambda r: f"[{r['log10(C_a)_p05']:.2f}, {r['log10(C_a)_p50']:.2f}, {r['log10(C_a)_p95']:.2f}]", axis=1),
        "log10(C_m)\n[p05, p50, p95]": df.apply(lambda r: f"[{r['log10(C_m)_p05']:.2f}, {r['log10(C_m)_p50']:.2f}, {r['log10(C_m)_p95']:.2f}]", axis=1),
        "P(C_m > C_a)": df["P(C_m > C_a)"].map(lambda x: f"{x:.3f}".rstrip("0").rstrip(".")),
    })

    fig, ax = plt.subplots(figsize=(16, 4.8))
    ax.axis("off")

    tab = ax.table(
        cellText=out.values,
        colLabels=out.columns,
        cellLoc="center",
        colLoc="center",
        loc="center",
    )

    tab.auto_set_font_size(False)
    tab.set_fontsize(11)
    tab.scale(1, 2.1)

    col_widths = [0.42, 0.22, 0.22, 0.14]
    for (row, col), cell in tab.get_celld().items():
        if col < len(col_widths):
            cell.set_width(col_widths[col])
        if row == 0:
            cell.set_text_props(weight="bold")
            cell.set_height(cell.get_height() * 1.15)

    for r in range(1, len(out) + 1):
        cell = tab[(r, 0)]
        cell.get_text().set_ha("left")
        cell.PAD = 0.02

    fig.tight_layout()
    fig.savefig(args.out_png, dpi=300, bbox_inches="tight")
    print(f"Wrote: {args.out_png}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
