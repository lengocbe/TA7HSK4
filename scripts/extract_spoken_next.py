"""Read-only OCR of the four supplied follow-on spoken Chinese books."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]
STARTS={'basic-upper':[1,11,22,33,43,56,66,76,87,97,108,120],
'basic-lower':[1,13,23,35,46,56,68,80,91,102,115,127],
'intermediate':[1,13,27,40,54,67,80,93,106,120,135,150,163,176],
'advanced':[1,9,18,26,34,49,58,65,72,80,94,103,111,120,128,142,151,159,168,176]}
OFFSETS={'basic-upper':12,'basic-lower':12,'intermediate':12,'advanced':14}
if __name__=='__main__':
 import argparse
 import pymupdf as f,numpy as np
 from rapidocr_onnxruntime import RapidOCR
 from build_spoken_next import BOOKS
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('book',choices=STARTS)
 parser.add_argument('--source-dir',type=Path,required=True,help='Folder containing the four original PDF files')
 args=parser.parse_args();sys.stdout.reconfigure(encoding='utf-8');key=args.book
 out=ROOT/'tmp/spoken-next';out.mkdir(parents=True,exist_ok=True)
 d=f.open(args.source_dir/BOOKS[key][2])
 ocr=RapidOCR(intra_op_num_threads=1,inter_op_num_threads=1,rec_batch_num=16)
 pages=sorted(set(s+OFFSETS[key]+k for s in STARTS[key] for k in range(8 if key=='intermediate' else 4)))
 for p in pages:
  dest=out/f'{key}-{p:03}.json'
  if dest.exists():continue
  pix=d[p-1].get_pixmap(matrix=f.Matrix(1.5,1.5));result,_=ocr(np.frombuffer(pix.samples,dtype=np.uint8).reshape(pix.height,pix.width,pix.n),use_cls=False)
  dest.write_text(json.dumps([dict(text=r[1],confidence=float(r[2]),box=r[0]) for r in result or []],ensure_ascii=False,indent=2),encoding='utf-8')
  print(key,p,flush=True)
