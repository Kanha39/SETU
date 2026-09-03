# Data Dictionary — merged_projects.csv

18,601 rows across three project statuses: **Ongoing** (18,213), **Completed** (375), **Frozen or Deleted** (13).

No rows were dropped and no nulls were imputed in this dataset. Missingness is
preserved as-is and, where relevant, flagged in a companion column so the ML
team can choose their own imputation/exclusion strategy.

---

## A. Original columns (carried over from source data)

| Column | Type | Known at project approval? | Notes |
|---|---|---|---|
| `project_code` | string | — | Unique-ish identifier; alphanumeric (e.g. `705735`, `N24001700`). Same code can repeat across reporting periods within Ongoing. |
| `project_name` | string | Yes | Free text. |
| `agency` | string | Yes | Implementing agency. |
| `state` | string | Yes | 5 nulls remain — unresolved, need manual lookup. |
| `date_of_approval` | date | Yes | ~7% null in Ongoing; ~0% in usable Completed rows. |
| `start_date` | date | Yes | ~4% null in Ongoing. |
| `target_doc` | date | Yes | Planned date of completion. ~2.6% null in Ongoing. |
| `revised_doc` | date | **No** | Only exists once a schedule has been revised. ~30% null — this is *expected*, not missing data (a project only gets a revised date if it was actually revised). |
| `actual_doc` | date | **No** | True completion date. 99.4% null overall — only ever populated for a subset of Completed projects (107 of 375). This is the single most target-relevant column and the scarcest one. |
| `original_cost_cr` | float | Yes | Sanctioned cost at approval, in ₹ Crore. |
| `revised_cost_cr` | float | **No** | Revised sanctioned cost. Null for all `Frozen or Deleted` rows and part of `Completed` (structural, source never captured it there) — see Section C. |
| `cumulative expenditure in rs. crore` | float | **No** | Actual money spent to date — a live snapshot, not a final figure, especially for Ongoing projects. Distinct from `revised_cost_cr` (see below). 2 rows have negative values (data error, flagged). |
| `physical progress (in percentage)` | float | **No** | Self-reported completion %, 0–100. |
| `ministry` | string | Yes | <1% null; null for all `Frozen or Deleted` (structural). |
| `sector` | string | Yes | No nulls. |
| `status` | string | — | `Ongoing` / `Completed` / `Frozen or Deleted`. **Do not use as a model feature** — for cost-overrun prediction specifically, status is confounded with the structural nulls in `revised_cost_cr` (i.e. it trivially predicts whether the target is missing, not the target's value). |

---

## B. Added columns — targets

| Column | Formula | Non-null rows | Purpose |
|---|---|---|---|
| `cost_overrun_abs_cr` | `revised_cost_cr - original_cost_cr` | 18,383 | Absolute overrun in ₹ Crore. |
| `cost_overrun_pct` | `cost_overrun_abs_cr / original_cost_cr` | 18,383 | Overrun as a percentage of original budget — usually the more comparable target across projects of different sizes. |
| `delay_actual_days` | `actual_doc - target_doc` (days) | **107 only** | "True" delay. Very small sample — likely too small to train on alone; consider as a validation/sanity-check set rather than the primary target. |
| `delay_proxy_days` | `revised_doc - target_doc` (days) | 12,914 | Proxy delay — measures "was the schedule revised," not "was the project actually late." Much larger sample. Recommended primary delay target unless the small `delay_actual_days` set is deliberately preferred. |

**Do not use `revised_cost_cr`, `revised_doc`, `actual_doc`, or `cumulative expenditure`
as model *features*** for these two targets — they are either the target itself or only
known after the outcome you're trying to predict (leakage risk). Kept in the dataset for
transparency, but the modeling team should exclude them from the feature set at training time.

---

## C. Added columns — missingness flags

Boolean columns, `True` where the source column is null. No imputation performed —
these exist so the ML team can decide their own strategy (drop, impute, or use the
flag itself as a feature, since missingness may be informative rather than random).

`date_of_approval_is_missing`, `start_date_is_missing`, `actual_doc_is_missing`,
`target_doc_is_missing`, `revised_doc_is_missing`, `revised_cost_cr_is_missing`,
`ministry_is_missing`, `state_is_missing`

**Important — structural vs. genuine nulls:**
- `Frozen or Deleted` (13 rows) never had `start_date`, `actual_doc`, `target_doc`,
  `revised_doc`, `revised_cost_cr`, or `ministry` collected — 100% null by design in that
  source, not missing-at-random.
- Part of `Completed` (116 of 375 rows, sourced from a separate quarterly file) has the
  same structural gap for the same columns.
- Nulls in `Ongoing` for `date_of_approval` / `start_date` / `target_doc` (single-digit %)
  are the genuinely "missing" cases worth investigating, since that source normally
  captures them.

---

## D. Added columns — expenditure vs. cost/progress signals

| Column | Formula | Purpose |
|---|---|---|
| `expenditure_to_original_cost_ratio` | `cumulative expenditure / original_cost_cr` | How much of the original budget has been spent. |
| `expenditure_to_revised_cost_ratio` | `cumulative expenditure / revised_cost_cr` | How much of the *current* approved budget has been spent. |
| `expenditure_exceeds_revised_cost` | `expenditure > revised_cost_cr` (bool) | Flags projects whose actual spend has already overtaken the officially revised budget while (potentially) still ongoing — a stronger red flag than `cost_overrun_pct` alone, since it's based on real cash outflow, not just a paper revision. |
| `expenditure_progress_mismatch` | `expenditure_to_original_cost_ratio - (physical_progress / 100)` | Continuous score: positive = spending is outpacing delivered work; negative = work is ahead of spend. |
| `high_spend_low_progress_flag` | `progress <= 20% AND expenditure_to_original_cost_ratio >= 0.8` (bool) | Convenience flag for the sharpest mismatch case (39 rows currently). **Threshold is a suggested default, not fixed** — adjust as needed. |

Note on interpretation (for the modeling team, not resolved here): a high mismatch score
could mean genuine overrun-in-progress, legitimate front-loaded costs (land acquisition,
equipment), or a `physical progress` field that simply isn't updated as often as
expenditure. The flag surfaces the pattern; it doesn't diagnose the cause.

---

## E. Added columns — data-quality flags

| Column | Meaning |
|---|---|
| `negative_expenditure_flag` | `cumulative expenditure < 0` (2 rows). Genuine data error, not a modeling signal — recommend excluding or correcting via lookup before use. |
| `negative_cost_overrun_flag` | `revised_cost_cr < original_cost_cr` (2,549 rows). Not necessarily an error — a project's sanctioned cost can be revised *down* (de-scoping, cost savings) — but worth the modeling team's awareness since "overrun" models often implicitly assume the overrun is non-negative. |

---
