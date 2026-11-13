"""Execute predeclared jobs, preserving each run and failures."""
import concurrent.futures,json,subprocess,sys,time,datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=json.loads((ROOT/'coursework/study_plan.json').read_text())
def job(seed,i,n):
 out=ROOT/'coursework/results'/f'main_n{n}_seed{seed}_k1_offset{i}'
 if (out/'status.json').exists():
  return json.loads((out/'status.json').read_text())
 out.mkdir(parents=True,exist_ok=True)
 start=time.monotonic()
 status=dict(iterations=n,offset=i,seed=seed,started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 try:
  with (out/'console.log').open('w') as f:
   subprocess.run([sys.executable,'coursework/run.py','--study','main','--seed',str(seed),'--iterations',str(n),'--limit','1','--offset',str(i)],cwd=ROOT,stdout=f,stderr=subprocess.STDOUT,timeout=P['search_timeout_seconds'],check=True)
   status['search_wall_seconds']=time.monotonic()-start
   subprocess.run([sys.executable,'coursework/evaluate.py',str(out)],cwd=ROOT,stdout=f,stderr=subprocess.STDOUT,timeout=P['evaluation_timeout_seconds'],check=True)
  status['status']='complete'
 except Exception as e:
  status.update(status='failed',error=type(e).__name__)
  status.setdefault('search_wall_seconds',time.monotonic()-start)
 status['total_wall_seconds']=time.monotonic()-start
 (out/'status.json').write_text(json.dumps(status,indent=2))
 print(json.dumps(status),flush=True)
 return status
if __name__=='__main__':
 # Alternate which budget starts first; pair same examples without shared memory.
 jobs=[(seed,i,n) for seed in P['seeds'] for i in P['indices'] for n in (P['iterations'] if (seed+i)%2 else list(reversed(P['iterations'])))]
 with concurrent.futures.ThreadPoolExecutor(max_workers=P['concurrency']) as pool:
  results=list(pool.map(lambda x:job(*x),jobs))
 (ROOT/'coursework/results/main_status.json').write_text(json.dumps(results,indent=2))
