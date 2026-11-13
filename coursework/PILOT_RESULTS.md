# Pilot results: LiTS with DeepSeek Flash

Completed 4 November 2026. Frozen dataset indices 0-4; one local seed (42); identical settings apart from iteration budget. All 10 jobs and upstream answer evaluations completed. Local verification checked dataset hash, coverage, and matching condition manifests.

| Metric | Baseline: 10 iterations | Modification: 3 iterations |
|---|---:|---:|
| Correct under upstream numeric scorer | 4/5 (80%) | 3/5 (60%) |
| Search LLM calls | 184 | 103 |
| Search input tokens | 214,605 | 79,794 |
| Search output tokens | 25,623 | 12,348 |
| Total search tokens | 240,228 | 92,142 |
| Sum of per-job search wall time | 358.02 s | 180.81 s |
| Evaluation LLM calls (separate) | 5 | 4 |

Reducing iterations saved 61.6% of search tokens in this pilot, with one additional task failure. The harder parentheses question produced no terminal answer at 3 iterations and the correct answer (4) at 10. Four easier tasks required little search, so one question dominates the difference. Concurrent execution makes wall time noisy; the table sums job times, not elapsed batch duration.

## Evaluation caveat
Both conditions predicted `42 inches` for reference `42` on index 1. The unchanged upstream numeric checker marked both incorrect because it does not remove unit text. Human inspection identifies a correct magnitude, but that does not overwrite the recorded primary metric. With that one formatting mismatch manually accepted as a separate diagnostic, the totals would be 5/5 and 4/5. A future evaluation change must be specified before new runs and applied consistently to both conditions.

## What this establishes
The authors' multi-step search pipeline runs with the declared DeepSeek compatibility setup; saved outputs can be evaluated; and the isolated iteration-budget modification has a measurable cost/accuracy tradeoff on this small sample. It does not establish statistical significance or directly reproduce the paper's 37% result. Model, reward scorer, sample size, current code version, stopping sample count, and output cap differ from the paper.

## Next experiment
Before collecting final report numbers, predeclare the numeric-answer evaluation policy, keep this pilot separate, select a fixed larger subset, and run 3 independent trials per condition (local seeds 42, 43, 44). Report mean and sample variance, preserve API nondeterminism and truncation limitations, and include the debug diary. No final-study results, variance estimates, or significance claims exist yet.

## Evidence
- [Per-question metrics](results/pilot_metrics.csv)
- [Aggregate machine-readable results](results/pilot_summary.json)
- [Completion statuses](results/pilot_status.json)
- [Run instructions](README.md)
- [Debug diary](DEBUG_DIARY.md)
- [Original paper, Table 6](https://aclanthology.org/2026.acl-demo.5.pdf)
