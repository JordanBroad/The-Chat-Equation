#!/usr/bin/env python3
"""
Plot Appendix C heatmap + regime map from a precomputed dataset.

Expected input format (CSV long-form):
  columns: A, log10E, E, S, dominant, delta

Outputs (default):
  - figures/AppendixC_heatmap_aligned_share.png
  - figures/AppendixC_regime_map_S_ge_0p5.png
"""
from __future__ import annotations

import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def pivot_grid(df: pd.DataFrame):
    # Ensure sorted axes
    A_vals = np.sort(df["A"].unique())
    logE_vals = np.sort(df["log10E"].unique())
    # pivot to 2D matrices
    S = df.pivot(index="log10E", columns="A", values="S").loc[logE_vals, A_vals].values
    dom = df.pivot(index="log10E", columns="A", values="dominant").loc[logE_vals, A_vals].values
    return A_vals, logE_vals, S, dom

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in_csv", default="data/AppendixC_heatmap_dataset.csv")
    ap.add_argument("--out_heatmap", default="figures/AppendixC_heatmap_aligned_share.png")
    ap.add_argument("--out_regime", default="figures/AppendixC_regime_map_S_ge_0p5.png")
    args = ap.parse_args()

    df = pd.read_csv(args.in_csv)

    required = {"A", "log10E", "S"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    if "dominant" not in df.columns:
        df = df.copy()
        df["dominant"] = np.where(df["S"] >= 0.5, 1, 0)

    A_vals, logE_vals, S, dom = pivot_grid(df)

    # Heatmap of S
    fig, ax = plt.subplots(figsize=(8.5, 6))
    im = ax.imshow(
        S,
        origin="lower",
        aspect="auto",
        extent=[A_vals.min(), A_vals.max(), logE_vals.min(), logE_vals.max()],
    )
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label("Aligned share S = C_a/(C_a + C_m)")

    ax.set_xlabel("Alignment probability A")
    ax.set_ylabel("log10(E)")
    ax.set_title("Appendix C: Aligned share S(A, E)")

    # Boundary contour S=0.5
    try:
        A_grid, logE_grid = np.meshgrid(A_vals, logE_vals)
        ax.contour(A_grid, logE_grid, S, levels=[0.5], linewidths=1.5)
    except Exception:
        pass

    fig.tight_layout()
    fig.savefig(args.out_heatmap, dpi=300, bbox_inches="tight")
    print(f"Wrote: {args.out_heatmap}")

    # Regime map (binary)
    fig2, ax2 = plt.subplots(figsize=(8.5, 6))
    im2 = ax2.imshow(
        dom,
        origin="lower",
        aspect="auto",
        extent=[A_vals.min(), A_vals.max(), logE_vals.min(), logE_vals.max()],
    )
    cbar2 = fig2.colorbar(im2, ax=ax2)
    cbar2.set_label("Dominant regime (1=aligned, 0=misaligned)")

    ax2.set_xlabel("Alignment probability A")
    ax2.set_ylabel("log10(E)")
    ax2.set_title("Appendix C: Regime map (S ≥ 0.5)")

    fig2.tight_layout()
    fig2.savefig(args.out_regime, dpi=300, bbox_inches="tight")
    print(f"Wrote: {args.out_regime}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
