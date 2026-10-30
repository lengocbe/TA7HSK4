"""Cache glossary OCR for the supplied Global Success 6, 8 and 9 scans."""
from pathlib import Path
import json,sys
import pymupdf as f,numpy as np
from rapidocr_onnxruntime import RapidOCR
ROOT=Path(__file__).resolve().parents[1];cache=ROOT/'tmp/english-grades';out=cache/'ocr';out.mkdir(exist_ok=True)
ocr=RapidOCR(intra_op_num_threads=1,inter_op_num_threads=1,rec_batch_num=16)
for book in [int(a) for a in sys.argv[1:]]:
 spec=next(s for s in json.loads((ROOT/'content/english-grades/sources.json').read_text(encoding='utf-8')) if s['book']==book);doc=f.open(Path('X:/TA6789')/spec['file'])
 pages={1:[71,72],2:[72,73],3:[137,138,139,140],4:[138,139,140,141]}[book]
 for n in pages:
  dest=out/f'{book}-{n}.json'
  if dest.exists():continue
  pg=doc[n-1];pix=pg.get_pixmap(matrix=f.Matrix(3,3));rs,_=ocr(np.frombuffer(pix.samples,dtype=np.uint8).reshape(pix.height,pix.width,pix.n),use_cls=False)
  dest.write_text(json.dumps(dict(book=book,page=n,file=spec['file'],width=pix.width,height=pix.height,rows=[dict(text=r[1],confidence=float(r[2]),box=r[0]) for r in rs or []]),ensure_ascii=False,indent=2),encoding='utf-8');print(book,n,flush=True)
