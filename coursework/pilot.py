"""Run the frozen five-item, two-condition pilot; each job has a 15min bound."""
import concurrent.futures,json,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def job(n,i):
 out=ROOT/'coursework/results'/f'pilot_n{n}_seed42_k1_offset{i}'
 out.mkdir(parents=True,exist_ok=True)
 start=time.monotonic()
 status={'iterations':n,'offset':i}
 try:
  with (out/'console.log').open('w') as f:
   cmd=[sys.executable,'coursework/run.py','--iterations',str(n),'--limit','1','--offset',str(i)]
   subprocess.run(cmd,cwd=ROOT,stdout=f,stderr=subprocess.STDOUT,timeout=900,check=True)
   status['search_wall_seconds']=time.monotonic()-start
   subprocess.run([sys.executable,'coursework/evaluate.py',str(out)],cwd=ROOT,stdout=f,stderr=subprocess.STDOUT,timeout=120,check=True)
  status['status']='complete'
 except Exception as e: status.update(status='failed',error=type(e).__name__)
 status['total_wall_seconds']=time.monotonic()-start
 (out/'status.json').write_text(json.dumps(status,indent=2))
 print(json.dumps(status),flush=True)
 return status
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
  result=list(pool.map(lambda x:job(*x),[(n,i) for i in range(5) for n in (3,10)]))
 (ROOT/'coursework/results/pilot_status.json').write_text(json.dumps(result,indent=2))
