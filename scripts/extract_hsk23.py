"""Cache OCR with page coordinates for review of the scanned source books."""
from pathlib import Path
import json,sys
import pymupdf as fitz
import numpy as np
from rapidocr_onnxruntime import RapidOCR
sys.stdout.reconfigure(encoding='utf-8')
root=Path(__file__).resolve().parents[1];out=root/'tmp/hsk23';out.mkdir(parents=True,exist_ok=True)
ocr=RapidOCR(intra_op_num_threads=2,inter_op_num_threads=1,rec_batch_num=16)
starts={2:[15,23,31,39,47,55,63,71,79,87,95,103,111,119,127],3:[17,27,36,45,53,62,71,80,88,97,106,114,123,132,141,151,159,167,173,182]}
for level in [2,3]:
 doc=fitz.open(f'D:/LeNgocBE/Download/Telegram Desktop/Giáo trình chuẩn HSK{level}.pdf')
 targets=sorted(set([8,10,12]+([14] if level==3 else [])+[n+k for n in starts[level] for k in range(1,3)]))
 if level==3:targets=sorted(set(targets+list(range(168,173))+list(range(192,204))))
 for page_number in targets:
  i=page_number-1;page=doc[i]
  dest=out/f'hsk{level}-{i+1:03}.json'
  if dest.exists():continue
  pix=page.get_pixmap(matrix=fitz.Matrix(1.8,1.8))
  result,_=ocr(np.frombuffer(pix.samples,dtype=np.uint8).reshape(pix.height,pix.width,pix.n),use_cls=False)
  rows=[dict(text=r[1],confidence=float(r[2]),box=r[0]) for r in (result or [])]
  dest.write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
  print('OCR HSK',level,'page',i+1,flush=True)
 print('Completed HSK',level,flush=True)
