"""Read-only OCR cache for the supplied HSK 6 textbooks."""
from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]
STARTS={'6.1':[14,24,33,44,54,65,74,85,96,107,116,126,136,147,156,167,178,188,197,207], '6.2':[14,23,33,42,52,62,71,81,92,103,112,122,134,143,154,165,176,187,198,208]}
if __name__=='__main__':
 import pymupdf as fitz
 import numpy as np
 from rapidocr_onnxruntime import RapidOCR
 sys.stdout.reconfigure(encoding='utf-8')
 out=ROOT/'tmp/hsk6';out.mkdir(parents=True,exist_ok=True)
 ocr=RapidOCR(intra_op_num_threads=2,inter_op_num_threads=1,rec_batch_num=16)
 for book,starts in STARTS.items():
  if len(sys.argv)>1 and sys.argv[1]!='extra' and book!=sys.argv[1]:continue
  doc=fitz.open(f'D:/LeNgocBE/Download/Telegram Desktop/Giáo trình chuẩn HSK{book}.pdf')
  targets=[s+4 for s in starts] if 'extra' in sys.argv else [8,10]+[s+k for s in starts for k in [1,2,3,4]]
  for p in sorted(set(targets)):
   dest=out/f'{book}-{p:03}.json'
   if dest.exists():continue
   pix=doc[p-1].get_pixmap(matrix=fitz.Matrix(2,2))
   result,_=ocr(np.frombuffer(pix.samples,dtype=np.uint8).reshape(pix.height,pix.width,pix.n),use_cls=False)
   dest.write_text(json.dumps([dict(text=r[1],confidence=float(r[2]),box=r[0]) for r in (result or [])],ensure_ascii=False,indent=2),encoding='utf-8')
   print(book,p,flush=True)
