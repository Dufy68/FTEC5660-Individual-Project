# LiTS search-budget reproduction

Status: five-item, one-trial pilot complete; see PILOT_RESULTS.md. Final multi-trial study and submission artifacts remain.

Question: Does reducing MCTS iterations from 10 to 3 preserve accuracy while reducing token consumption?

Paper: https://aclanthology.org/2026.acl-demo.5.pdf (Section 3.3, Table 6).
Upstream: https://github.com/xinzhel/lits-llm
Commit: 25e94d862cb4514c22d9a80a635e392461769df7.

The paper reports 37% for ReST MCTS on the first 100 numeric-answer MATH500 items, using Llama3-8B-Instruct and an RLHFlow reward model. Its 10 iterations and branching factor 3 motivate our baseline.

This is an adapted reproduction: DeepSeek Flash is used for policy and generative reward scoring. It cannot directly validate the paper's 37% number. Current code, termination behavior, and reward implementation may also differ. Document these differences.

Fixed settings: upstream ConcatPolicy, ConcatTransition, GenerativePRM, MCTSSearch; same dataset order (pilot first 5 items); branching 3; max depth 10; rollout depth 2; max output 512; binary-sampling termination (one sample per check); no early stop on first solution; no memory or continuation; thinking disabled; correctness reward samples 2 and usefulness samples 1 without chain-of-thought.

Treatment variable only: n_iters 10 versus 3. Planned local trial seeds: 42, 43, 44; API sampling may remain nondeterministic. Freeze dataset IDs before measured runs. Pilot establishes feasibility, not statistical evidence.

Measure accuracy, API tokens, call count, wall-clock time. Retain raw traces and per-item predictions. Missing answers count as incorrect. Separate evaluation cost from search cost. No reference labels go to search policy/reward model. Report mean and sample variance across trials.

Target: reproduce the claimed runnable multi-step math search pipeline under declared substitutions, then measure the isolated iteration-budget modification. Compare Table 6 descriptively under unequal conditions.

Remaining submission: measured results; report <=10 pages; clean GitHub repository with install/run steps; recorded Zoom presentation <=15 minutes (user records).
