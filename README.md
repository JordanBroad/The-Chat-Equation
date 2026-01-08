# Code (reproducibility)

This folder contains small, dependency-light scripts to reproduce key figures from the *The Chat Equation* repository.

## Quick start

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate
pip install -r requirements.txt
```

## Appendix C (heatmap / regime map)

```bash
python code/plot_appendix_c.py --in_csv data/AppendixC_heatmap_dataset.csv
```

## Appendix D (Monte Carlo summary table figure)

```bash
python code/make_appendix_d_table.py --in_csv figures/AppendixD_monte_carlo_summary_tightened.csv
```
