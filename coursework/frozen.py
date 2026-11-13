"""Frozen data; the numeric correctness check is upstream, unchanged."""
import json
from pathlib import Path
from lits.benchmarks.registry import register_dataset,register_evaluator
from lits_benchmark.math_qa_eval import evaluate_math_qa
@register_dataset('course_math500',task_type='language_grounded')
def load_frozen():
    return json.loads((Path(__file__).parent/'data/math500-numeric.json').read_text())
register_evaluator('course_math500')(evaluate_math_qa)
