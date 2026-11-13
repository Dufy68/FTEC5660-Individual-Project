# FTEC5660: LiTS reproduction and search-budget modification

This folder contains an individual reproducibility experiment using the authors' LiTS code. See [PLAN.md](PLAN.md) for the target, scope, and limitations.

## Setup
Python 3.12 was used. From the repository root:

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r coursework/requirements-api.lock
.venv/bin/python -m pip install -e . --no-deps
```

The upstream package requires a Python version of at least 3.11.

The lock file describes the tested API-only environment. It intentionally omits optional local-model, memory, and geospatial dependencies declared by the broader upstream package; do not use it for those features.

Set `DEEPSEEK_API_KEY` in your environment, or point `COURSE_ENV_FILE` at a local `.env` containing that variable. On the current computer the runner defaults to the existing HW2 credential file. Secrets are read into memory, not saved in experiment configs. Never commit a credential file.

## Data
`data/math500-numeric.json` freezes the authors' 316-item numeric MATH500 derivative. `data/provenance.json` records the Hugging Face revision and SHA-256. Both conditions use source-order indices 0 through 4 for the pilot. The full benchmark solutions remain in the source dataset; the search runner supplies only questions to policy and reward components.

## Run

```sh
.venv/bin/python coursework/run.py --iterations 3 --limit 1 --offset 0 --dry-run
.venv/bin/python coursework/pilot.py
.venv/bin/python coursework/summarize.py
.venv/bin/python coursework/verify.py
```

The pilot runs both iteration budgets on five questions with at most five concurrent jobs. Each search job has a 15-minute wall timeout, and each evaluation has a 2-minute timeout. Check `results/pilot_status.json` for failures. Do not rerun into existing output folders when collecting independent trials: upstream resumes existing terminal files and appends some logs. Preserve or rename an earlier run first.

Individual runs accept `--iterations 3|10`, `--limit`, `--offset`, and `--seed`. Evaluation:

```sh
.venv/bin/python coursework/evaluate.py coursework/results/pilot_n3_seed42_k1_offset0
```

Search logs and evaluation logs are separate. Evaluation uses the current upstream answer-voting tool call plus unchanged numeric checking. A missing answer is incorrect. Do not infer accuracy from an answer appearing somewhere in a trace. Avoid repeated evaluation when measuring cost; it appends fresh evaluation calls.

## Compatibility and controlled modification
The DeepSeek compatibility patch sends the provider's documented `thinking.type` setting. Both conditions disable thinking. The experimental modification is solely `n_iters=10` to `n_iters=3`. Both conditions use the same generative reward model, binary-sampling termination (one sample), 512 policy output tokens, branch factor 3, max depth 10, rollout depth 2, and no early stop on first solution.

## Limits of comparison
The paper used Llama3-8B-Instruct and an RLHFlow reward model. We substitute DeepSeek Flash and a generative scorer; the code is also a newer upstream commit. These results are not directly comparable to the paper's Table 6. The five-question pilot assesses feasibility, not statistical significance. Additional seeds and a larger fixed subset are needed for the report.

Raw debugging runs are excluded from measured summaries. `pilot_metrics.csv` contains per-question measured outcomes; `pilot_summary.json` aggregates completed runs only. Check each condition has all five items before treating it as a complete pilot.

## Pilot interpretation
The 512-token cap prevents the observed length-validation retry loop, but can truncate longer reasoning. Treat this as an additional model/setup limitation, not proof that the search algorithm cannot solve a task. Local seeds do not control DeepSeek server-side randomness. Concurrent requests also make runtime comparisons noisy.

Full raw traces remain in each local run folder. Compact metrics, manifests, outcomes, and statuses are versioned; bulky search/evaluation logs are excluded from Git. Re-running the documented commands regenerates them.

## Results
See [the completed pilot analysis](PILOT_RESULTS.md). The upstream strict scorer gives 4/5 at 10 iterations versus 3/5 at 3 iterations. A shared unit-format mismatch is disclosed separately. These are pilot results only.
