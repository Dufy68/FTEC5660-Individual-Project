"""Summarize measured artifacts; never substitute invented outputs."""
import csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
rows=[]
for p in sorted((ROOT/'results').glob('pilot_n*_seed42_k1_offset*')):
 if not (p/'status.json').exists(): continue
 status=json.loads((p/'status.json').read_text())
 if status['status']!='complete': continue
 outcomes=json.loads((p/'outcomes.json').read_text())
 if len(outcomes)!=1: raise ValueError(f'Expected one outcome: {p}')
 logs=[json.loads(x) for x in (p/'search/inferencelogger.log').read_text().splitlines() if x.strip()]
 ev=[json.loads(x) for x in (p/'evaluation/inferencelogger.log').read_text().splitlines() if x.strip()]
 o=outcomes[0]
 rows.append(dict(iterations=status['iterations'],index=o['index'],unique_id=o['unique_id'],correct=int(o['correct']),prediction=o['prediction'],reference=o['reference'],terminals=o['terminals'],search_calls=len(logs),input_tokens=sum(x['input_tokens'] for x in logs),output_tokens=sum(x['output_tokens'] for x in logs),search_wall_seconds=round(status['search_wall_seconds'],2),eval_calls=len(ev),eval_input_tokens=sum(x['input_tokens'] for x in ev),eval_output_tokens=sum(x['output_tokens'] for x in ev)))
if not rows: raise SystemExit('No completed measured runs yet.')
with (ROOT/'results/pilot_metrics.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
summary={}
for n in (3,10):
 r=[x for x in rows if x['iterations']==n]
 summary[n]={'completed':len(r),'correct':sum(x['correct'] for x in r),'accuracy':sum(x['correct'] for x in r)/len(r) if r else None,**{k:sum(x[k] for x in r) for k in ['search_calls','input_tokens','output_tokens','search_wall_seconds','eval_calls','eval_input_tokens','eval_output_tokens']}}
(ROOT/'results/pilot_summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
