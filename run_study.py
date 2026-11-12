"""Mutation-score comparison of test-design techniques against seeded bugs.

Usage:  python run_study.py
Writes to results/: summary.md, summary_<sut>.csv, kill_matrix_<sut>.csv, mutation_scores.png
"""
import csv
import importlib
import os
import statistics

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from harness import passes_order, passes_ship, suite_kills
from mutants import ORDER_MUTANTS, SHIPPING_MUTANTS, order_impls, shipping_impls
from suites import order_suites, shipping_suites

SEED = 42          # base seed for the random baseline
REPEATS = 1000     # random suites generated per size
RESULTS = "results"


def load_human():
    try:
        mod = importlib.import_module("suites.my_suite")
        return mod.SHIPPING_CASES, mod.ORDER_CASES
    except ModuleNotFoundError:
        return None, None


def evaluate(name, mutant_info, impls, techniques, passes, random_suite):
    """Score every suite and compare it with random suites of the same size."""
    ids = list(impls)
    rows, matrix = [], {}
    for suite_name, cases in techniques.items():
        killed = {m for m in ids if suite_kills(cases, impls[m], passes)}
        matrix[suite_name] = killed
        n = len(cases)
        scores = []
        for r in range(REPEATS):
            rnd = random_suite(n, SEED * 100_000 + n * 1_000 + r)
            scores.append(sum(suite_kills(rnd, impls[m], passes) for m in ids) / len(ids))
        score = len(killed) / len(ids)
        rows.append({
            "suite": suite_name,
            "tests": n,
            "killed": len(killed),
            "mutants": len(ids),
            "score_%": round(100 * score, 1),
            "random_same_size_mean_%": round(100 * statistics.mean(scores), 1),
            "random_sd_%": round(100 * statistics.pstdev(scores), 1),
            "random_>=_suite_%": round(100 * sum(s >= score for s in scores) / REPEATS, 1),
            "survivors": " ".join(sorted(set(ids) - killed)) or "-",
        })
    # write CSVs
    with open(os.path.join(RESULTS, f"summary_{name}.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    with open(os.path.join(RESULTS, f"kill_matrix_{name}.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["mutant", "description"] + list(techniques))
        for m in ids:
            w.writerow([m, mutant_info[m][0]] + ["killed" if m in matrix[s] else "SURVIVED" for s in techniques])
    return rows


def md_table(rows):
    cols = list(rows[0])
    out = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(r[c]) for c in cols) + " |")
    return "\n".join(out)


def main():
    os.makedirs(RESULTS, exist_ok=True)
    ship_tech = dict(shipping_suites.TECHNIQUES)
    order_tech = dict(order_suites.TECHNIQUES)
    hs, ho = load_human()
    if hs is not None:
        ship_tech["Your suite"] = hs
        order_tech["Your suite"] = ho

    ship_rows = evaluate("shipping", SHIPPING_MUTANTS, shipping_impls(), ship_tech,
                         passes_ship, shipping_suites.random_suite)
    order_rows = evaluate("order", ORDER_MUTANTS, order_impls(), order_tech,
                          passes_order, order_suites.random_suite)

    with open(os.path.join(RESULTS, "summary.md"), "w", encoding="utf-8") as fh:
        fh.write("### Shipping fee calculator (14 seeded bugs)\n\n" + md_table(ship_rows) + "\n\n")
        fh.write("### Order state machine (10 seeded bugs)\n\n" + md_table(order_rows) + "\n\n")
        fh.write(f"Random baseline: {REPEATS} random suites of the same size per row, base seed {SEED}. "
                 "`random_>=_suite_%` = share of random suites that did at least as well.\n")

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    for ax, rows, title in ((axes[0], ship_rows, "Shipping fee"), (axes[1], order_rows, "Order state machine")):
        x = range(len(rows))
        ax.bar(x, [r["score_%"] for r in rows], label="technique suite")
        ax.errorbar(x, [r["random_same_size_mean_%"] for r in rows],
                    yerr=[r["random_sd_%"] for r in rows], fmt="o", color="black",
                    capsize=4, label="random, same size (mean ± sd)")
        ax.set_xticks(list(x))
        ax.set_xticklabels([f'{r["suite"]}\n(n={r["tests"]})' for r in rows], rotation=30, ha="right", fontsize=8)
        ax.set_ylim(0, 105)
        ax.set_ylabel("Mutation score (%)")
        ax.set_title(title)
        ax.legend(loc="lower right", fontsize=8)
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS, "mutation_scores.png"), dpi=150)

    print(open(os.path.join(RESULTS, "summary.md"), encoding="utf-8").read())


if __name__ == "__main__":
    main()
