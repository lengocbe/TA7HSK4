"""Read-only OCR of vocabulary and dialogue pages in the two supplied scans."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]
STARTS={'upper':[1,8,15,22,30,40,49,58,69,79,91,102,115,129,141],'lower':[1,14,25,38,50,64,78,89,105,121,133,151,165,176,186]}
PREFIX={'upper':'01_汉语口语速成入门篇上_','lower':'02_汉语口语速成入门篇下_'}
if __name__=='__main__':
 import pymupdf as fitz,numpy as np
 from rapidocr_onnxruntime import RapidOCR
 sys.stdout.reconfigure(encoding='utf-8');book=sys.argv[1]
 paths=list(Path('D:/LeNgocBE/Download/Telegram Desktop').glob(PREFIX[book]+'*.pdf'));assert len(paths)==1
 doc=fitz.open(paths[0]);out=ROOT/'tmp/spoken';out.mkdir(exist_ok=True)
 ocr=RapidOCR(intra_op_num_threads=2,inter_op_num_threads=1,rec_batch_num=16)
 first=int(sys.argv[2]) if len(sys.argv)>2 else 0
 last=int(sys.argv[3]) if len(sys.argv)>3 else 15
 for p in sorted(set(s+11+k for i,s in enumerate(STARTS[book]) if first<=i<last for k in range(STARTS[book][i+1]-s if book=='upper' and i<5 else 4))):
  path=out/f'{book}-{p:03}.json'
  if path.exists():continue
  pix=doc[p-1].get_pixmap(matrix=fitz.Matrix(1.6,1.6));result,_=ocr(np.frombuffer(pix.samples,dtype=np.uint8).reshape(pix.height,pix.width,pix.n),use_cls=False)
  path.write_text(json.dumps([dict(text=r[1],confidence=float(r[2]),box=r[0]) for r in (result or [])],ensure_ascii=False,indent=2),encoding='utf-8')
  print(book,p,flush=True)
