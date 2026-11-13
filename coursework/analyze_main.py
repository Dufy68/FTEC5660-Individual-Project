"""Compute full-study metrics with the predeclared denominator and failures."""
import csv,json,statistics,hashlib
from pathlib import Path
root=Path(__file__).resolve().parent
plan=json.loads((root/'study_plan.json').read_text())
data=json.loads((root/'data/math500-numeric.json').read_text())
rows=[]
for seed in plan['seeds']:
 for n in plan['iterations']:
  for i in plan['indices']:
   p=root/f'results/main_n{n}_seed{seed}_k1_offset{i}'
   if not (p/'status.json').exists(): raise SystemExit(f'Study still running: {p.name}')
   status=json.loads((p/'status.json').read_text())
   outcome=json.loads((p/'outcomes.json').read_text()) if (p/'outcomes.json').exists() else []
   if status['status']=='complete': assert len(outcome)==1 and outcome[0]['index']==i
   o=outcome[0] if outcome else {}
   def records(path):return [json.loads(x) for x in path.read_text().splitlines() if x.strip()] if path.exists() else []
   search=records(p/'search/inferencelogger.log');ev=records(p/'evaluation/inferencelogger.log')
   assert not any(x.get('cached') for x in search),'Cached replay invalidates independent trial'
   r=dict(seed=seed,iterations=n,index=i,unique_id=data[i]['unique_id'],level=data[i]['level'],subject=data[i]['subject'],status=status['status'],prediction=o.get('prediction',''),normalized_prediction=o.get('normalized_prediction',''),reference=data[i]['answer'],correct=int(bool(o.get('correct',False)) and status['status']=='complete'),magnitude_correct=int(bool(o.get('magnitude_correct',False)) and status['status']=='complete'),terminals=o.get('terminals',0),search_calls=len(search),input_tokens=sum(x['input_tokens'] for x in search),output_tokens=sum(x['output_tokens'] for x in search),search_wall_seconds=status['search_wall_seconds'],evaluation_calls=len(ev),evaluation_input_tokens=sum(x['input_tokens'] for x in ev),evaluation_output_tokens=sum(x['output_tokens'] for x in ev),policy_outputs_at_cap=sum(x['output_tokens']>=512 and x['role'].startswith('policy') for x in search))
   r['search_tokens']=r['input_tokens']+r['output_tokens'];rows.append(r)
for i in plan['indices']:
 for seed in plan['seeds']:
  manifests=[json.loads((root/f'results/main_n{n}_seed{seed}_k1_offset{i}/manifest.json').read_text()) for n in plan['iterations']]
  for m in manifests:m.pop('iterations')
  assert manifests[0]==manifests[1]
trials=[]
for seed in plan['seeds']:
 for n in plan['iterations']:
  rr=[r for r in rows if r['seed']==seed and r['iterations']==n]
  trials.append(dict(seed=seed,iterations=n,accuracy=statistics.mean(x['correct'] for x in rr),magnitude_accuracy=statistics.mean(x['magnitude_correct'] for x in rr),failures=sum(x['status']!='complete' for x in rr),**{k:sum(x[k] for x in rr) for k in ['search_tokens','input_tokens','output_tokens','search_calls','search_wall_seconds','evaluation_calls','evaluation_input_tokens','evaluation_output_tokens','policy_outputs_at_cap']}))
summary={}
for n in plan['iterations']:
 rr=[r for r in trials if r['iterations']==n]
 summary[str(n)]={'trials':3,'distinct_questions':10,'evaluations':30}
 for k in ['accuracy','magnitude_accuracy','search_tokens','search_calls','search_wall_seconds']:
  vals=[r[k] for r in rr];summary[str(n)][k]={'mean':statistics.mean(vals),'sample_variance':statistics.variance(vals),'sample_sd':statistics.stdev(vals),'by_trial':vals}
 for k in ['input_tokens','output_tokens','evaluation_calls','evaluation_input_tokens','evaluation_output_tokens','policy_outputs_at_cap','failures']:
  summary[str(n)][k+'_total']=sum(r[k] for r in rr)
summary['search_token_reduction']=1-summary['3']['search_tokens']['mean']/summary['10']['search_tokens']['mean']
summary['primary_accuracy_difference_3_minus_10']=summary['3']['accuracy']['mean']-summary['10']['accuracy']['mean']
summary['cost_ceiling_usd']=sum((r['input_tokens']+r['evaluation_input_tokens'])*0.3/1e6+(r['output_tokens']+r['evaluation_output_tokens'])*1.2/1e6 for r in rows)
for name,rr in [('main_metrics.csv',rows),('main_trials.csv',trials)]:
 with (root/'results'/name).open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rr[0]));w.writeheader();w.writerows(rr)
(root/'results/main_summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
