"""Check frozen data, completed result coverage, and the isolated treatment."""
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parent
meta=json.loads((root/'data/provenance.json').read_text())
assert hashlib.sha256((root/'data/math500-numeric.json').read_bytes()).hexdigest()==meta['sha256']
for i in range(5):
 conditions=[]
 for n in (3,10):
  p=root/f'results/pilot_n{n}_seed42_k1_offset{i}'
  status=json.loads((p/'status.json').read_text());assert status['status']=='complete'
  outcomes=json.loads((p/'outcomes.json').read_text());assert len(outcomes)==1 and outcomes[0]['index']==i
  m=json.loads((p/'manifest.json').read_text());assert m['iterations']==n and m['offset']==i
  # Raw configs are optional in a clean clone; compare compact manifests too.
  m.pop('iterations');conditions.append(m)
 assert conditions[0]==conditions[1],f'Uncontrolled setting difference at {i}'
print('Verified frozen dataset hash, all 10 outcomes, and matched condition manifests.')
