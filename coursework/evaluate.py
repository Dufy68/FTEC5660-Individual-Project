"""Evaluate saved terminals with upstream voting and numeric checker."""
import sys,os,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'demos')]
from dotenv import dotenv_values
v=dotenv_values(os.environ.get('COURSE_ENV_FILE','/Users/dukefengyu/Codex/FTEC5660-HW2-main/.env'))
os.environ['OPENAI_API_KEY']=os.environ.get('DEEPSEEK_API_KEY') or v['DEEPSEEK_API_KEY']
os.environ['OPENAI_API_BASE']='https://api.deepseek.com'
os.environ['LITS_NETWORK_RECOVERY_TIMEOUT']='30'
from lits.cli.eval_search import load_terminal_nodes_from_file
from lits.eval.search import evaluate_search_result
from lits.lm import get_lm,setup_inference_logging
from lits_benchmark.math_qa_eval import evaluate_math_qa
out=Path(sys.argv[1]).resolve()
rows=json.loads((ROOT/'coursework/data/math500-numeric.json').read_text())
model=get_lm('openai/deepseek-flash',enable_thinking=False)
setup_inference_logging(model,root_dir=str(out/'evaluation'),override=False)
results=[]
for p in sorted((out/'search/terminal_nodes').glob('*.json')):
 d=load_terminal_nodes_from_file(p);idx=d['query_idx']
 r=evaluate_search_result(d['terminal_nodes'],d['query'],rows[idx]['answer'],task_type='language_grounded',voting_model=model,custom_evaluator=evaluate_math_qa)
 results.append(dict(index=idx,unique_id=rows[idx]['unique_id'],reference=rows[idx]['answer'],terminals=len(d['terminal_nodes']),**r))
(out/'outcomes.json').write_text(json.dumps(results,indent=2))
print(json.dumps(results))
