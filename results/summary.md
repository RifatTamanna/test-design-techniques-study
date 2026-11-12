### Shipping fee calculator (14 seeded bugs)

| suite | tests | killed | mutants | score_% | random_same_size_mean_% | random_sd_% | random_>=_suite_% | survivors |
|---|---|---|---|---|---|---|---|---|
| Equivalence partitioning | 10 | 4 | 14 | 28.6 | 40.1 | 6.5 | 98.0 | S01 S02 S03 S04 S05 S07 S08 S11 S13 S14 |
| Boundary value analysis | 16 | 10 | 14 | 71.4 | 43.5 | 4.6 | 0.0 | S10 S11 S13 S14 |
| Decision table | 8 | 5 | 14 | 35.7 | 38.1 | 8.0 | 79.9 | S01 S02 S03 S04 S05 S06 S07 S08 S14 |
| Full combination | 24 | 6 | 14 | 42.9 | 45.1 | 4.0 | 95.1 | S01 S02 S03 S04 S05 S07 S08 S12 |
| EP + BVA + decision table | 30 | 13 | 14 | 92.9 | 46.1 | 3.8 | 0.0 | S14 |

### Order state machine (10 seeded bugs)

| suite | tests | killed | mutants | score_% | random_same_size_mean_% | random_sd_% | random_>=_suite_% | survivors |
|---|---|---|---|---|---|---|---|---|
| Valid transitions only | 5 | 2 | 10 | 20.0 | 30.2 | 9.8 | 94.7 | O01 O02 O03 O04 O06 O08 O09 O10 |
| Invalid transitions only | 15 | 9 | 10 | 90.0 | 58.1 | 13.0 | 1.4 | O05 |
| All state/event pairs | 20 | 10 | 10 | 100.0 | 68.6 | 12.5 | 1.0 | - |

Random baseline: 1000 random suites of the same size per row, base seed 42. `random_>=_suite_%` = share of random suites that did at least as well.
