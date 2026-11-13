"""Bounded, logged coursework runs using the upstream LiTS CLI."""
import argparse, json, os, random, runpy, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser()
p.add_argument('--iterations',type=int,choices=[3,10],default=10)
p.add_argument('--limit',type=int,default=5)
p.add_argument('--offset',type=int,default=0)
p.add_argument('--seed',type=int,default=42)
p.add_argument('--study',choices=['pilot','main'],default='pilot')
p.add_argument('--dry-run',action='store_true')
a=p.parse_args()
if not 1<=a.limit<=100: p.error('limit must be 1..100')
from dotenv import dotenv_values
values=dotenv_values(os.environ.get('COURSE_ENV_FILE','/Users/dukefengyu/Codex/FTEC5660-HW2-main/.env'))
os.environ['OPENAI_API_KEY']=os.environ.get('DEEPSEEK_API_KEY') or values['DEEPSEEK_API_KEY']
os.environ['OPENAI_API_BASE']='https://api.deepseek.com'
os.environ['LITS_NETWORK_RECOVERY_TIMEOUT']='30'
os.environ['HF_HUB_DISABLE_TELEMETRY']='1'
os.environ['MPLCONFIGDIR']=str(ROOT/'.cache/matplotlib')
import numpy as np
import torch
random.seed(a.seed); np.random.seed(a.seed); torch.manual_seed(a.seed)
out=ROOT/'coursework/results'/f'{a.study}_n{a.iterations}_seed{a.seed}_k{a.limit}_offset{a.offset}'

if not a.dry_run and (out/'search/terminal_nodes').exists() and any((out/'search/terminal_nodes').iterdir()):
    raise SystemExit('Output already contains a run; use a fresh directory or archive it first.')
out.mkdir(parents=True,exist_ok=True)
manifest=dict(offset=a.offset,policy_temperature=0.7,iterations=a.iterations,limit=a.limit,seed=a.seed,model='deepseek-flash',base_url='https://api.deepseek.com',thinking=False,top_p=1,max_new_tokens=512,upstream_commit='25e94d862cb4514c22d9a80a635e392461769df7',note='Adapted reproduction; hosted API sampling is not guaranteed seed-deterministic.')
(out/'manifest.json').write_text(json.dumps(manifest,indent=2))
os.chdir(ROOT)
sys.path.insert(0,str(ROOT)); sys.path.insert(0,str(ROOT/'demos'))
sys.argv=['lits-search','--include','coursework.frozen','--dataset','course_math500','--policy-model','openai/deepseek-flash','--eval-model','openai/deepseek-flash','--policy','concat','--transition','concat','--reward','generative','--search-arg',f'n_iters={a.iterations}','n_actions=3','max_steps=10','roll_out_steps=2','sample_size_terminate=1','terminate_constraints=[binary_sampling]','terminate_on_first_solution=false','runtime_limit_before_iter=600','enable_think_policy=false','enable_think_eval=false','enable_think_terminal_gen=false','--component-arg','max_new_tokens=512','n_for_correctness=2','n_for_usefulness=1','think_for_correctness=false','think_for_usefulness=false','--var',f'limit={a.limit}',f'offset={a.offset}','--output-dir',str(out/'search')]
if a.dry_run: sys.argv.append('--dry-run')
runpy.run_module('lits.cli.search',run_name='__main__')
