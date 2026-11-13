# Debug diary

- System Python was too old for LiTS; switched to isolated Python 3.12.
- Upstream declares many dependencies for unrelated backends. Installed and locked the API-only path; pinned compatible boto3/aioboto3 versions after dependency resolution conflicted.
- Network access required approved network-enabled commands for GitHub, Hugging Face, and DeepSeek.
- Saved HW2 DeepSeek key authenticated successfully. Available API model IDs were deepseek-flash and deepseek-v4-pro. No key copied or printed.
- Provider docs say old Flash aliases now use DeepSeek-V4.1-Flash-1017. Record deepseek-flash explicitly; endpoint results can change over time.
- Upstream's generic custom-endpoint thinking switch was vLLM-specific. Added explicit DeepSeek thinking.type support, applied equally to both conditions.
- CLI list parser retained literal quotes in terminate_constraints=["step_signal"]. Correct syntax is unquoted list members, e.g. [binary_sampling].
- Thinking settings belong in --search-arg, not --cfg. Unknown --cfg settings generated warnings. Interrupted that debugging run and excluded it from results.
- Free-form policy output did not set the structured termination flag. A step_signal smoke run saved no terminal nodes, although the correct answer appeared in the trace. Evaluator correctly marked it wrong. Use upstream binary_sampling termination, with one sample per check in both pilot conditions. This differs from upstream's default sample count and must be disclosed.
- Froze exact dataset revision and row order before the measured pilot. The derivative contains 316 numeric-answer items, not all 500 MATH500 tasks.

- First measured pilot with 1024-token cap completed four items per condition; the fifth repeatedly exceeded the upstream 1000-token validation threshold. Stopped all remaining calls. Reduced output cap to 512 in both conditions and reran the complete fixed pilot. Prior artifacts carry debug_cap1024_ prefixes and are excluded from measured summaries.

- Final upstream scoring flagged `42 inches` versus reference `42` in both conditions. Preserved that mismatch in the primary metric and documented manual magnitude agreement separately. Earlier progress updates described correctness before all numeric-checking outputs were inspected; final results are 4/5 and 3/5.
