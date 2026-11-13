from pathlib import Path
import hashlib,json
from datasets import load_dataset
from huggingface_hub import HfApi
root=Path(__file__).resolve().parent
revision=HfApi().dataset_info('xinzhel/math500-float').sha
rows=list(load_dataset('xinzhel/math500-float',split='test',revision=revision))
p=root/'data/math500-numeric.json';p.parent.mkdir(exist_ok=True)
p.write_text(json.dumps(rows,ensure_ascii=False,indent=2))
(root/'data/provenance.json').write_text(json.dumps(dict(repository='xinzhel/math500-float',revision=revision,split='test',rows=len(rows),sha256=hashlib.sha256(p.read_bytes()).hexdigest()),indent=2))
print('Frozen',len(rows),'rows; revision',revision)
